
import ccxt

class Ohlcv:
  def __init__(self, symbol, timeframe, since, limit):
    self.symbol = symbol
    self.timeframe = timeframe
    self.since = since
    self.limit = limit

    binance = ccxt.binance()
    # return
    # self.ohlcv = binance.fetch_ohlcv(symbol=self.symbol, timeframe=self.timeframe, since=self.since, limit=self.limit)
    self.ohlcv = binance.fetch_ohlcv(symbol=self.symbol, timeframe=self.timeframe, limit=self.limit)
    
    


# binance = ccxt.binance()
# ohlcv = binance.fetch_ohlcv(symbol='ETH/BTC', timeframe='5m', since=1653559688, limit=12)
