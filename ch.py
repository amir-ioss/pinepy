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
import websockets

from _help import highest, lowest, atr__, pine_rma, ema

class HKA:

    def __init__(self, coin):
        interval = '5m'
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
        
        # ATR Period
        length = 22
        # ATR Multiplier
        mult = 3.0

        dir = 1

        # store prevs
        longStops = []
        shortStops = []
        dirs = []
        placeOrder = False
        buyPrice = 0



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
        self.rsi = talib.RSI(self.df['Close'], timeperiod = length)
        self.sma = talib.SMA(self.df['HKClose'], timeperiod=length)
        self.rsiMa = talib.SMA(self.rsi, timeperiod=14)
        self.atr = talib.ATR(self.df['HKHigh'], self.df['HKLow'], self.df['HKClose'], timeperiod=length)
        # self.pine_rma = pine_rma(self.df, 22)
        # p(ema(np.nan_to_num(self.df['HKClose'].to_numpy()), 14))
        # p(talib.EMA(self.df['HKClose'].to_numpy(), 14))
        

        for idx in range(len(self.kandles)):
            # _closes = self.df['Close'].to_numpy()
            _closes = np.nan_to_num(self.df['HKClose'].to_numpy())
            _current_close = _closes[:idx+1] 

            close = _closes[idx]
            time = datetime.fromtimestamp(self.kandles[idx][0]/1000)

            atr = mult * self.atr[idx]
            longStop = highest(_current_close, length) - atr
            longStops.append(longStop)

            # play
            # p(self.df['HKOpen'][idx],self.df['HKHigh'][idx], self.df['HKLow'][idx],  self.df['HKClose'][idx], 
            #  "-----")
            # p(format(close,'.4f'),"<---->",  round(atr, 4))

            shortStop = lowest(_current_close, length) + atr
            shortStops.append(shortStop)

            if idx < 2 : continue
            
            #   long
                # longStopPrev = nz(longStop[1], longStop) 
                # longStop := close[1] > longStopPrev ? max(longStop, longStopPrev) : longStop
            longStopPrev = longStop if math.isnan(float(longStops[-2])) else longStops[-2]
            longStop = max(longStop, longStopPrev) if _closes[idx-1] > longStopPrev else longStop

            #   short
                # shortStopPrev = nz(shortStop[1], shortStop)
                # shortStop := close[1] < shortStopPrev ? math.min(shortStop, shortStopPrev) : shortStop
            shortStopPrev = shortStop if math.isnan(float(shortStops[-2])) else shortStops[-2]
            shortStop = min(shortStop, shortStopPrev) if _closes[idx-1] < shortStopPrev else shortStop

            dir = 1 if close > shortStopPrev else -1 if close < longStopPrev else dir
            dirs.append(dir)


            if(len(dirs)>3):
                buySignal = dir == 1 and dirs[-2] == -1
                # if(buySignal and not placeOrder):
                if(buySignal):
                    placeOrder = True
                    buyPrice  = close
                    p("~GREEN","BUY",  time, "==>",close)

            if(len(dirs)>3):
                sellSignal = dir == -1 and dirs[-2] == 1
                if(sellSignal):
                    placeOrder = False
                    profit  = close - buyPrice
                    p("~RED", "SELL", time, "==>", f"|| profit :({close}-{buyPrice})", profit, " ||")


            __color =  "~RED" if close < self.kandles[idx][6] else "~GREEN"
            __colorRsi =  "~RED" if  self.rsi[idx] < self.rsiMa[idx] else "~BLUE"
            # p(time, __color,  format(close,'.4f'),  "~END" , __colorRsi, format(self.rsi[idx],'.0f'),  format(self.rsiMa[idx],'.0f'))

        # p(self.kandles)
        p(datetime.fromtimestamp(self.kandles[0][0]/1000), "======",len(self.kandles))
        # p("----", dirs)




bot = HKA({"symbol": "XRP/USDT"})
bot.run()

