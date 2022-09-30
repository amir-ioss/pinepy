
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib

import calendar
from datetime import datetime

# import modules
from ohlcv import Ohlcv


# print(talib.__version__)
# df = pd.read_json('purchases.json')


ohlcv_ = Ohlcv('ETH/BTC', '5m', 1653559688, 50)
ohlcv = ohlcv_.ohlcv

df = pd.DataFrame(ohlcv, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])

start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)
end_dt = datetime.fromtimestamp(ohlcv[-1][0]/1000)


# df['Time'] = [datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
# df.set_index('Time', inplace=True)

# ohlcv.info()
# df = pd.DataFrame(ohlcv)
# arr = df["Close"].to_numpy()

# print(df.tail(1))


# df["Volume"].plot(kind = 'line',  x = 'Time', y = 'Low')
# df["High"].plot(kind = 'line',  x = 'Time', y = 'High')
# df["Low"].plot(kind = 'line',  x = 'Time', y = 'High')

# plt.show()



# x = np.arange(0, 5, 0.1)
# y = np.sin(x)
# plt.plot(x, y)
# plt.show()



from talib import abstract

data_length = 50

inputs = {
    # 'high': np.random.random(data_length),
    'open': df['Open'].to_numpy(),
    'high': df['High'].to_numpy(),
    'low': df['Low'].to_numpy(),
    'close': df['Close'].to_numpy(),
    'volume': df['Volume'].to_numpy()
}
           

# directly
SMA = abstract.SMA
# AVGPRICE = abstract.AVGPRICE
# output = SMA(inputs, timeperiod=5)
# output = talib.SMA(close, timeperiod =25)
avrg_price = talib.AVGPRICE(df['Open'].to_numpy(), df['High'].to_numpy(), df['Low'].to_numpy(), df['Close'].to_numpy())
median_price = talib.MIDPRICE( df["High"].to_numpy(),  df["Low"].to_numpy())
sma = SMA(inputs, timeperiod=5)
rsi = talib.RSI(df['Close'].to_numpy(), timeperiod=14)

# print(np.greater_equal(avrg_price, median_price))

print(rsi[-1])



plt.plot(avrg_price)
plt.plot(median_price)

# plt.show()

# print(avrg_price, median_price)
# print(median_price)



def number_to_string(argument):
    print(argument)
    if argument == '0': return 'as'
    else: return "no args"
 


import sys


def main():
    argv = len(sys.argv)
    print(number_to_string(sys.argv[1]))
    


if __name__ == "__main__":
   main()