# Cryptocurrency Data

## Retrieve data from Crypto Data Download

Period can be hour ('h') or daily ('d')

```
from tensortrade.data.cdd import CryptoDataDownload
from tensortrade.oms.instruments import USD, BTC, ETH

cdd = CryptoDataDownload()

data = cdd.fetch("Bitstamp", "USD", "BTC", "1h")

df = data.copy()

# df.describe()

plt.plot(df['date'], df['close'])

df.head()
```