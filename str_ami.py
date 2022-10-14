from datetime import datetime
import math
from time import sleep
import talib
import json
import calendar
import pandas as pd
import numpy as np
import client
from log import p 

from _help import highest, lowest, atr__, pine_rma, ema

class str_ami:
    def __init__(self, kandles):
        self.kandles = kandles
        self.run()

    def run(self):
        
        # store prevs
        _signals=[]
        _profits = []
        _order=[]

        
        buyPrice = 0
        placeOrder = False
        enter = False
        exit_ = False
        showBox = False

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

            if idx < 2 : 
                _order.append(placeOrder)
                continue
                 
            # play
            # p(self.df['HKOpen'][idx],self.df['HKHigh'][idx], self.df['HKLow'][idx],  self.df['HKClose'][idx], 
            #  "-----")
            signal = talib.EMA(np.nan_to_num(_signals), timeperiod = 9)
            # p(format(close,'.4f'),"<---->",  placeOrder)

              # // var isBullish = false
            isTrend = (self.rsiMA[idx] - self.rsiMA[idx-1]) > 0.05
            macdSupport = macd > signal[idx]
           

            # enter
            if self.rsi[idx] > self.rsiMA[idx]:
                enter = True


            if enter and isTrend and macdSupport and not placeOrder:
                placeOrder = True
                buyPrice = _opens[idx]
                self.buyTime = self.kandles[idx][0]
                # p("~GREEN","BUY",  time, "==>",close)

            # exit
            if self.rsi[idx] <= self.rsiMA[idx] and placeOrder:
                placeOrder = False
                # showBox = True 
                enter = False
                profit  = close - buyPrice
                status = "~GREEN" if profit > 0  else "~RED"
                # p("~RED", "SELL", time, "==>", f" profit :({close}-{buyPrice})", status,  profit)
                # p()
                _profits.append(profit)
                buyPrice = 0


            _order.append(placeOrder)

            # p(datetime.fromtimestamp(self.kandles[idx][0]/1000), "---", placeOrder, _order[-2])
            # p(time, __color,  format(close,'.4f'),  "~END" )

        # p(self.kandles)
        # p(datetime.fromtimestamp(self.kandles[0][0]/1000), "======",len(self.kandles))
        # p(_profits)
        
        
        #  FINAL OUT
        isBeginning = self.buyTime == self.kandles[-1][0] or  self.buyTime == self.kandles[-2][0]
        # # p(self.kandles[-1][6], "- new -", self.kandles[0][6])
        order = "BUY" if placeOrder else "SELL"
        p(order, self.buyTime, '--> ', self.kandles[-1][0], self.kandles[-2][0])
        # order = "BUY" if placeOrder and not _order[-2] else "SELL" if not placeOrder and _order[-2] else "AWAIT"  
        self.result = {"order": order, "buyPrice": buyPrice, "isBeginning": isBeginning, "candle": self.kandles[-1]}
