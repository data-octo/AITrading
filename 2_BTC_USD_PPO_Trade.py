from gym.spaces import Discrete

from tensortrade.env.default.actions import TensorTradeActionScheme

from tensortrade.env.generic import ActionScheme, TradingEnv
from tensortrade.core import Clock
from tensortrade.oms.instruments import ExchangePair
from tensortrade.oms.wallets import Portfolio
from tensortrade.oms.orders import (
    Order,
    proportion_order,
    TradeSide,
    TradeType
)

class BSH(TensorTradeActionScheme):
    ''' 
        action: {0: buy asset, 1: sell asset}
    '''
    registered_name = "bsh"

    def __init__(self, cash: 'Wallet', asset: 'Wallet'):
        super().__init__()
        self.cash = cash
        self.asset = asset

        self.listeners = []
        self.action = 0

    @property
    def action_space(self):
        return Discrete(2)

    def attach(self, listener):
        self.listeners += [listener]
        return self

    def get_orders(self, action: int, portfolio: 'Portfolio'):
        order = None

        if abs(action - self.action) > 0:
            src = self.cash if self.action == 0 else self.asset
            tgt = self.asset if self.action == 0 else self.cash
            order = proportion_order(portfolio, src, tgt, 0.2)
            self.action = action

        for listener in self.listeners:
            listener.on_action(action)

        return [order]

    def reset(self):
        super().reset()
        self.action = 0

from tensortrade.env.default.rewards import TensorTradeRewardScheme
from tensortrade.feed.core import Stream, DataFeed


class PBR(TensorTradeRewardScheme):

    registered_name = "pbr"

    def __init__(self, price: 'Stream'):
        super().__init__()
        self.position = -1

        r = Stream.sensor(price, lambda p: p.value, dtype="float").diff()
        position = Stream.sensor(self, lambda rs: rs.position, dtype="float")

        reward = (r * position).fillna(0).rename("reward")

        self.feed = DataFeed([reward])
        self.feed.compile()

    def on_action(self, action: int):
        self.position = -1 if action == 0 else 1

    def get_reward(self, portfolio: 'Portfolio'):
        return self.feed.next()["reward"]

    def reset(self):
        self.position = -1
        self.feed.reset()

import matplotlib.pyplot as plt

from tensortrade.env.generic import Renderer


class PositionChangeChart(Renderer):

    def __init__(self, color: str = "orange"):
        self.color = "orange"

    def render(self, env, **kwargs):
        history = pd.DataFrame(env.observer.renderer_history)

        actions = list(history.action)
        p = list(history.price)

        buy = {}
        sell = {}

        for i in range(len(actions) - 1):
            a1 = actions[i]
            a2 = actions[i + 1]

            if a1 != a2:
                if a1 == 0 and a2 == 1:
                    buy[i] = p[i]
                else:
                    sell[i] = p[i]

        buy = pd.Series(buy)
        sell = pd.Series(sell)

        fig, axs = plt.subplots(1, 2, figsize=(15, 5))

        fig.suptitle("Performance")

        axs[0].plot(np.arange(len(p)), p, label="price", color=self.color)
        axs[0].scatter(buy.index, buy.values, marker="^", color="green")
        axs[0].scatter(sell.index, sell.values, marker="^", color="red")
        axs[0].set_title("Trading Chart")
        
#         env.action_scheme.portfolio.performance.plot(ax=axs[1])
        performance = pd.DataFrame.from_dict(env.action_scheme.portfolio.performance, orient='index')
        columns = ['bitstamp:/USD:/free','bitstamp:/USD:/locked','bitstamp:/BTC:/free','bitstamp:/BTC:/locked','bitstamp:/BTC:/worth']
        performance.drop(columns, inplace=True, axis=1)
        
        performance.plot(ax=axs[1])
        axs[1].set_title("Net Worth")

        plt.show()

from tensortrade.data.cdd import CryptoDataDownload

cdd = CryptoDataDownload()

# df = cdd.fetch("Bitstamp", "USD", "BTC", "1h")
df = cdd.fetch("Bitstamp", "USD", "BTC", "d")

data = df.copy()


import ray
import numpy as np
import pandas as pd

from ray import tune
from ray.tune.registry import register_env

import tensortrade.env.default as default

from tensortrade.feed.core import DataFeed, Stream
from tensortrade.oms.exchanges import Exchange
from tensortrade.oms.services.execution.simulated import execute_order
from tensortrade.oms.wallets import Wallet, Portfolio
from tensortrade.oms.instruments import USD, BTC, ETH

def create_env(config):
    
    p = Stream.source(df.close, dtype="float").rename("USD-BTC")

    bitstamp = Exchange("bitstamp", service=execute_order)(
        p
    )

    cash = Wallet(bitstamp, 10000 * USD)
    asset = Wallet(bitstamp, 0.05 * BTC)

    portfolio = Portfolio(USD, [
        cash,
        asset
    ])

    feed = DataFeed([
       Stream.source(df['close'], dtype="float").rename("close"),
       Stream.source(df['open'], dtype="float").rename("open"),
       Stream.source(df['high'], dtype="float").rename("high"),
       Stream.source(df['low'], dtype="float").rename("low"),
       Stream.source(df['volume'], dtype="float").rename("volume"),
    ])

    reward_scheme = PBR(price=p)

    action_scheme = BSH(
        cash=cash,
        asset=asset
    ).attach(reward_scheme)

    renderer_feed = DataFeed([
        Stream.source(df['close'], dtype="float").rename("price"),
        Stream.sensor(action_scheme, lambda s: s.action, dtype="float").rename("action")
    ])
#     feed = DataFeed(streams)

#     renderer_feed = DataFeed([
#         Stream.source(price_history[c].tolist(), dtype="float").rename(c) for c in price_history]
#     )

    environment = default.create(
        feed=feed,
        portfolio=portfolio,
        action_scheme=action_scheme,
        reward_scheme=reward_scheme,
        renderer_feed=renderer_feed,
        renderer=PositionChangeChart(),
        window_size=config["window_size"],
        max_allowed_loss=0.2
    )
    return environment

register_env("TradingEnv", create_env)

checkpoint_path = '/Users/yuan/ray_results/PPO/PPO_TradingEnv_0_2021-05-07_21-33-29tqkn893y/checkpoint_5/checkpoint-5'
print(checkpoint_path)

ray.init(num_cpus = 1)

import ray.rllib.agents.ppo as ppo

# Restore agent
agent = ppo.PPOTrainer(
    env="TradingEnv",
    config={
        "env_config": {
            "window_size": 25
        },
        "framework": "torch",
        "log_level": "DEBUG",
        "ignore_worker_failures": True,
        "num_workers": 1,
        "num_gpus": 0,
        "clip_rewards": True,
        "lr": 8e-6,
        "lr_schedule": [
            [0, 1e-1],
            [int(1e2), 1e-2],
            [int(1e3), 1e-3],
            [int(1e4), 1e-4],
            [int(1e5), 1e-5],
            [int(1e6), 1e-6],
            [int(1e7), 1e-7]
        ],
        "gamma": 0,
        "observation_filter": "MeanStdFilter",
        "lambda": 0.72,
        "vf_loss_coeff": 0.5,
        "entropy_coeff": 0.01
    }
)
agent.restore(checkpoint_path)

df = data[-150:]
env = create_env({
    "window_size": 25
})

# Run until episode ends
episode_reward = 0
done = False
obs = env.reset()

# while not done:
for _ in range(len(df.index)):
    action = agent.compute_action(obs)
    obs, reward, done, info = env.step(action)
    print(reward)
    # print(env.observer.feed.next())
    episode_reward += reward

env.render()

from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

from pandasgui import show
performance = pd.DataFrame.from_dict(env.action_scheme.portfolio.performance, orient='index')

# copy performance data to clipboard for analysis using Number
# performance.to_clipboard(index=True)
performance.to_csv('result/BTC_USD_PPO_Performance_{}.csv'.format(today))
performance.plot()

gui = show(performance)

ledger = env.action_scheme.portfolio.ledger.as_frame()
ledger.to_csv('result/BTC_USD_PPO_ledger_{}.csv'.format(today))
ledger.plot()

gui = show(ledger)
