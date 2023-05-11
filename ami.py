import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import asyncio
from datetime import datetime
import time
from _help.ohlcv import Ohlcv
from _help.hkac import Hkac
import calendar
# from _help.order import order 
import requests

import talib
import json
import pandas as pd
import numpy as np
# from _help.log import p 
from data.data_test import test_data 
from data.dates import dates 
from data.coins import coins

# UTILS

def price_percentage(num, per = 0.1):
    return (num/100)*per

def percentage(num1, num2):
    return 100-((num1/num2)*100)

def tpsl_price(num, per = 0.1):
    return {"tp":num+price_percentage(num, per), "sl":num-price_percentage(num, per)}

def pivothigh(high: np.ndarray, left:int, right: int):
    pivots = np.roll(talib.MAX(high, left + 1 + right), -right)
    pivots[pivots != high] = np.NaN
    return pivots

def pivotlow(low: np.ndarray, left:int, right: int):
    pivots = np.roll(talib.MIN(low, left + 1 + right), -right)
    pivots[pivots != low] = np.NaN
    return pivots

class Boat:
    def __init__(self):
        self.count = 0
        self.oneTimeRun = False
        self.coins = coins
        self.dates = dates
        self.month = []
        pass

    def run(self,):
        while True:
            print("\n                         ---- scanning ({0})  ----\n".format(len(self.coins)))
            this_minute = datetime.today().minute
            abs_num = this_minute/5
            
            if abs_num == round(abs_num):
                print("TOP")
                

            else: 
                # print("SKIP NOW")
                # continue
                pass


            # for each coin 
            # for idx in range(len(self.coins)):
            for idx in range(len(self.dates)):
                # p("ON", self.coins[idx]['symbol'])


                interval = '5m'
                now = datetime.utcnow()
                unixtime = calendar.timegm(now.utctimetuple())
                since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
                # # start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)
                # date_test = self.dates[idx] #self.dates[idx] # "2022-12-29 00:00:00"
                # ohlcv_ = Ohlcv("XRP/USDT", interval, None, 300)
                # # ohlcv_ = Ohlcv(self.coins[idx]['symbol'], interval, date_test, 300)
                # kandles = Hkac(ohlcv_.ohlcv).kandles
                kandles = Hkac(test_data).kandles # TEST DATA
                # p(kandles)

                df = pd.DataFrame(kandles, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'HKOpen', 'HKHigh', 'HKLow', 'HKClose'])
                # indicators
                rsi_ = talib.RSI(df['HKClose'], timeperiod = 14)
                rsiMA_ = talib.SMA(rsi_, timeperiod = 14)
                rsi = np.nan_to_num(rsi_.to_numpy())
                rsiMA = np.nan_to_num(rsiMA_.to_numpy())
                # p(datetime.fromtimestamp(df['Time'][-1]/1000), "rsi", rsi[-1], "rsiMA", rsiMA[-1])
                time_ =  datetime.fromtimestamp(np.nan_to_num(df['Time'].to_numpy()[-1])/1000)
                close = np.nan_to_num(df['Close'].to_numpy())
                _open = np.nan_to_num(df['Open'].to_numpy())
                hkclose = np.nan_to_num(df['HKClose'].to_numpy())
                # macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
                # print("rsi:", rsi[-1], "rsiMA:", rsiMA[-1], "macd:", macd[-1], "macdsignal:", macdsignal[-1])

                LEFT_BAR = 21
                RIGHT_BAR = 21
                hhs = pivothigh(close, LEFT_BAR, RIGHT_BAR)
                lls = pivotlow(close, LEFT_BAR, RIGHT_BAR)

                isOrderPlaced = False
                
                trades=[]
                entryPrice = 0
                exitPrice = 0
                INVEST = 10
                FEE = 0.04 
                LEVERAGE = 20

                # EXPLORING
                hh = [0]
                ll = [0]
                farFrom = 0
                breakout =  False
                # breakoutEntry =  False

                for index in range(len(df['Close'])):
                    if(index < 26):continue

                    time =  datetime.fromtimestamp(np.nan_to_num(df['Time'].to_numpy()[index])/1000)
                    closes_now = close[0: index]
                    # p_change = percentage(price1, price2) 
                    
                    # print(time, "high-",hh[index], "low-", ll[index])
                    if(not np.isnan(lls[index]) and ll[-1] != lls[index]):
                        # print(time,ll[-1], "last----POINT-------new", lls[index])
                        ll.append(lls[index])
                        # if(ll[-1]==0):
                        #     ll = [lls[index]]
                        # else:
                        #     ll.append(lls[index])
                        farFrom = 0
                    farFrom += 1

                    # breake out
                    breakout = True in (ele > _open[index] for ele in ll[1:])
                    # breakout = True if (_open[index] < min(ll)) else False 
                    # print(time, breakout)



                    # ENTRY ////////////////////////////////////////////////////////
                    last_ll_p = percentage(ll[-1], _open[index])
                    entry_common = not isOrderPlaced and farFrom > RIGHT_BAR
                    entry_height = last_ll_p < .05 and not -.05 > last_ll_p 
                    # print(time, last_ll_p)

                    tail_low = talib.MIN(closes_now)[-1]
                    tail_low_p = percentage(tail_low, _open[index])
                    # print(time,breakout, ll,  "tail_low_p", tail_low_p)
                    breakout_entry = True if (breakout and tail_low_p > .2) else False

                    # if(index > 26):
                    #     print("tail_low", talib.MIN(closes_now)[-1])

                    if(((entry_height and entry_common) or (breakout_entry and not isOrderPlaced))):
                        print("last point -", ll)
                        if(breakout_entry):
                            # breakoutEntry = True
                            ll = [tail_low]
                            print("###########", ll)
                        print(time,"ENTRY", _open[index])
                        isOrderPlaced = True
                        entryPrice = _open[index]
                        pass
                    

                    # EXIT /////////////////////////////////////////////////////////
                    p_change = percentage(entryPrice, _open[index])
                    if((p_change > 0.40 or -0.2 > p_change) and isOrderPlaced):
                        print(time,"EXIT", _open[index], f'{p_change:.2f}'+'%','\n')
                        isOrderPlaced = False
                        exitPrice = _open[index]
                        breakout = False

                        amount = INVEST/entryPrice
                        exit_size = amount*exitPrice
                       

                        # LEVERAGE
                        l_amount = amount*LEVERAGE
                        l_entry_size = INVEST*LEVERAGE
                        l_exit_size = exit_size*LEVERAGE

                        amount_entry_fee = price_percentage(l_entry_size, FEE)
                        amount_exit_fee = price_percentage(l_exit_size, FEE)
                        pl = (l_exit_size-l_entry_size)-(amount_entry_fee+amount_exit_fee)

                        INVEST = INVEST+pl
                        trades.append(pl)
                        # if(len(trades) == 3):exit()
                        pass

               # RESULTS //////////////////////////////////////////////////////////////////
                print(self.dates[idx], sum(trades), trades)
                self.month.append(sum(trades))

                exit()

            # end of testing
            print("MONTH PL-------->",sum(self.month))
            # self.month.clear()
            break


            
            

#  MAIN
bot = Boat()
bot.run()
# print(test_data)

# bot = Scalp({"symbol": "LUNC/USDT"}, '1m', 12.22)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(bot.run())

# loop.close()
