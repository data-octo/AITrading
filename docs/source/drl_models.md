# Reinforcement Learning models


```
from stable_baselines import SAC
from stable_baselines import PPO2
from stable_baselines import A2C
from stable_baselines import DDPG
from stable_baselines import TD3
from stable_baselines.ddpg.policies import DDPGPolicy
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
def train_A2C(env_train, model_name, timesteps=10000):
 “””A2C model”””
 start = time.time()
 model = A2C(‘MlpPolicy’, env_train, verbose=0)
 model.learn(total_timesteps=timesteps)
 end = time.time()
 model.save(f”{config.TRAINED_MODEL_DIR}/{model_name}”)
 print(‘Training time (A2C): ‘, (end-start)/60,’ minutes’)
 return model
def train_DDPG(env_train, model_name, timesteps=10000):
 “””DDPG model”””
 start = time.time()
 model = DDPG(‘MlpPolicy’, env_train)
 model.learn(total_timesteps=timesteps)
 end = time.time()
 model.save(f”{config.TRAINED_MODEL_DIR}/{model_name}”)
 print(‘Training time (DDPG): ‘, (end-start)/60,’ minutes’)
 return model
def train_PPO(env_train, model_name, timesteps=50000):
 “””PPO model”””
 start = time.time()
 model = PPO2(‘MlpPolicy’, env_train)
 model.learn(total_timesteps=timesteps)
 end = time.time()
 model.save(f”{config.TRAINED_MODEL_DIR}/{model_name}”)
 print(‘Training time (PPO): ‘, (end-start)/60,’ minutes’)
 return model
def DRL_prediction(model, test_data, test_env, test_obs):
 “””make a prediction”””
 start = time.time()
 for i in range(len(test_data.index.unique())):
   action, _states = model.predict(test_obs)
   test_obs, rewards, dones, info = test_env.step(action)
   # env_test.render()
 end = time.time()
 ```