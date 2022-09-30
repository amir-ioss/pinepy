from cmath import log
from datetime import datetime
import math
from time import sleep
from ohlcv import Ohlcv
import talib
import asyncio
import json
import calendar
import pandas as pd
import numpy as np
import client
from log import p 
from markets import markets

from _help import highest, lowest, atr__, pine_rma, ema

class HKA:

    def __init__(self, coin):
        interval = '1m'
        # numberOfCandles = 205
        numberOfCandles = 1000
        self.coin = coin

        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())
        since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
        # start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)

        ohlcv_ = Ohlcv(self.coin["symbol"], interval, None, None)
        # ohlcv_ = Ohlcv("DEGO/USDT", interval, since, numberOfCandles)
        self.kandles = ohlcv_.ohlcv

        

    def run(self):
        # print(self.kandles)
        # for idx, item in enumerate(self.kandles):

        # Open: (Open (previous candle) + Close (previous candle))/2
        # Close: (Open + Low + Close + High)/4
        # High: the same of the actual candle
        # Low: the same of the actual candle
        
        # store prevs
        placeOrder = False
        buyPrice = 0
        _signals=[]
        _profits = []
        
        placeOrder = False
        enter = False
        exit_ = False
        showBox = False



        for idx in range(len(self.kandles)):
            if idx < 1 : 
                self.kandles[idx].append(self.kandles[idx][1])
                self.kandles[idx].append(self.kandles[idx][2])
                self.kandles[idx].append(self.kandles[idx][3])
                self.kandles[idx].append(self.kandles[idx][4])
                continue

            # Heikin-Ashi

            # Candle	Regular Candlestick	Heikin Ashi Candlestick
            # Open	Open0	(HAOpen(-1) + HAClose(-1))/2
            # High	High0	MAX(High0, HAOpen0, HAClose0)
            # Low	Low0	MIN(Low0, HAOpen0, HAClose0
            # Close	Close0	(Open0 + High0 + Low0 + Close0)/4

            HKOpen = (self.kandles[idx-1][6] + self.kandles[idx-1][9]) / 2
            HKClose = (self.kandles[idx][1] + self.kandles[idx][2] + self.kandles[idx][3] + self.kandles[idx][4]) / 4
            HKHigh = max(self.kandles[idx][2], HKOpen, HKClose)
            HKLow = min(self.kandles[idx][3], HKOpen, HKClose)

            self.kandles[idx].append(HKOpen)
            self.kandles[idx].append(HKHigh)
            self.kandles[idx].append(HKLow)
            self.kandles[idx].append(HKClose)
            # p(HKOpen, HKHigh, HKLow, HKClose) 

        self.df = pd.DataFrame(self.kandles, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'HKOpen', 'HKHigh', 'HKLow', 'HKClose'])
        # indicators
        self.rsi = talib.RSI(self.df['HKClose'], timeperiod = 14)
        self.rsiMA = talib.SMA(self.rsi, timeperiod = 14) 

        # // MACD

        # fast_ma = ta.ema(close, 12)
        # slow_ma = ta.ema(close, 26)
        # macd = fast_ma - slow_ma
        # signal = ta.ema(macd, 9)

        self.fast_ma = talib.EMA(self.df['HKClose'], timeperiod = 12) 
        self.slow_ma = talib.EMA(self.df['HKClose'], timeperiod = 26) 

        
        

        for idx in range(len(self.kandles)):
            # _closes = self.df['Close'].to_numpy()
            _closes = np.nan_to_num(self.df['HKClose'].to_numpy())
            _opens = np.nan_to_num(self.df['HKOpen'].to_numpy())
            _current_close = _closes[:idx+1] 
            macd =  self.fast_ma[idx] -  self.slow_ma[idx]
            _signals.append(macd)

            close = _closes[idx]
            time = datetime.fromtimestamp(self.kandles[idx][0]/1000)

            if idx < 2 : continue
                 
                        # play
            # p(self.df['HKOpen'][idx],self.df['HKHigh'][idx], self.df['HKLow'][idx],  self.df['HKClose'][idx], 
            #  "-----")
            signal = talib.EMA(np.nan_to_num(_signals), timeperiod = 9)
            # p(format(close,'.8f'),"<---->",  self.rsi[idx], self.rsiMA[idx])
            # p(time, format(close,'.8f'),"<---->",  placeOrder)

              # // var isBullish = false
            isTrend = (self.rsiMA[idx] - self.rsiMA[idx-1]) > 0.05
            macdSupport = macd > signal[idx]
           

            # enter
            if self.rsi[idx] > self.rsiMA[idx]:
                enter = True

            # p(enter , isTrend , macdSupport , placeOrder)

            if enter and isTrend and macdSupport and not placeOrder:
                placeOrder = True
                buyPrice = _opens[idx]
                p("~GREEN","BUY",  time, "==>",close)

            # exit
            if self.rsi[idx] <= self.rsiMA[idx] and placeOrder:
                exit_ = True
                placeOrder = False
                enter = False
                # showBox = True 
                profit  = close - buyPrice
                status = "~GREEN" if profit > 0  else "~RED"
                p("~RED", "SELL", time, "==>", f" profit :({close}-{buyPrice})", status,  profit)
                p()
                _profits.append(profit)


            # if(len(dirs)>3):
            #     buySignal = dir == 1 and dirs[-2] == -1
            #     # if(buySignal and not placeOrder):
            #     if(buySignal):
            #         placeOrder = True
            #         buyPrice  = close
            #         p("~GREEN","BUY",  time, "==>",close)

            # if(len(dirs)>3):
            #     sellSignal = dir == -1 and dirs[-2] == 1
            #     if(sellSignal):
            #         placeOrder = False
            #         profit  = close - buyPrice
            #         p("~RED", "SELL", time, "==>", f"|| profit :({close}-{buyPrice})", profit, " ||")


            __color =  "~RED" if close < self.kandles[idx][6] else "~GREEN"
            __colorRsi =  "~RED" if  self.rsi[idx] < self.rsiMA[idx] else "~BLUE"
            # p(time, __color,  format(close,'.4f'),  "~END" , __colorRsi, format(self.rsi[idx],'.0f'),  format(self.rsiMa[idx],'.0f'))

        # p(self.kandles)
        p(datetime.fromtimestamp(self.kandles[0][0]/1000), "======",len(self.kandles))
        # p("----", dirs)
        # p(_profits)
        p(datetime.fromtimestamp(self.kandles[-1][0]/1000), self.kandles[-2][9])




bot = HKA({"symbol": "TRX/BUSD"})
bot.run()

# pr.filter(_=> _ > 0).reduce((a, b)=> Math.abs(a)+Math.abs(b), 0)