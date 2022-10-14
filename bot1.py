import asyncio
from datetime import datetime
import time
from ohlcv import Ohlcv
from hkac import Hkac
import calendar
from str_rsi import str_rsi 
from order import order 

import talib
import json
import pandas as pd
import numpy as np
from log import p 

class Scalp:
    def __init__(self, coin, interval='5m', invest = 12.22):
        self.interval = interval
        # numberOfCandles = 205
        numberOfCandles = 1000
        self.coin = coin
        self.invest = invest

        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())
        since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
        # start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)

        self.count = 0
        self.oneTimeRun = False
        self.placeOrder = False

        pass 

    async def run(self,):
        while True:
            # do something
            time.sleep(1) # wait 5 minutes
            this_minute = datetime.today().minute
            abs_num = this_minute/5

        
            # p(abs_num , self.count, self.oneTimeRun,  abs_num == self.count and not self.oneTimeRun, "else", abs_num != round(abs_num))
            
            # 1 min test
            abs_num = this_minute
            if self.count == 60 : self.count = 0
            if abs_num == self.count and not self.oneTimeRun: 
            # if abs_num == round(abs_num) and not self.oneTimeRun:
                #  new candles
                ohlcv_ = Ohlcv(self.coin["symbol"], self.interval, None, None)
                kandles = Hkac(ohlcv_.ohlcv).kandles
                
                # p("run again")
                strategy = str_rsi(kandles)
                price = strategy.result['candle'][4]
                amount = self.invest / price
                def msg(*args):
                    # p()
                    p(this_minute, "->", datetime.fromtimestamp(strategy.result['candle'][0]/1000), *args)
                # p(strategy.result)

                # CREATE ORDER
                if strategy.result['order'] == "BUY" and strategy.result['isBeginning'] and not self.placeOrder:
                # if strategy.result['order'] == "BUY" and not self.placeOrder:
                    msg("~BLUE","PALCE BUY ORDER", price)
                    # create buy order
                    order(self.coin["symbol"], 'market', 'buy', amount, {})
                    self.placeOrder = True

                elif strategy.result['order'] == "SELL" and self.placeOrder:
                    msg("~RED","PALCE SELL ORDER", price)
                    # create sell order
                    order(self.coin["symbol"], 'market', 'sell', amount, {})
                    self.placeOrder = False
                    
                else:
                    msg("no position found")
                
                self.oneTimeRun = True 
                pass

            # elif abs_num != round(abs_num): 
            elif abs_num != self.count : # 1 min test
                self.oneTimeRun = False
                # p(self.count, abs_num == round(abs_num), this_minute)

            self.count = this_minute+1



#  MAIN
bot = Scalp({"symbol": "TRX/USDT"}, '1m', 12.22)
# bot = Scalp({"symbol": "LUNC/USDT"}, '1m', 12.22)

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run())

# loop.close()

