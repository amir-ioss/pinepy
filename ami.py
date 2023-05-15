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

class Bot:
    def __init__(self, coin, interval='5m', invest = 10):
        self.count = 0
        self.oneTimeRun = False
        self.coins = coins
        self.coin = coin
        self.dates = dates
        self.month = []
        self.invest = invest
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
                logs = True

                # p("ON", self.coins[idx]['symbol'])


                interval = '5m'
                now = datetime.utcnow()
                unixtime = calendar.timegm(now.utctimetuple())
                since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
                # start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)
                date_test = self.dates[idx] #self.dates[idx] # "2023-02-05 00:00:00"
                ohlcv_ = Ohlcv(self.coin['symbol'], interval, date_test if not logs else "2023-03-22 00:00:00", 300)
                # ohlcv_ = Ohlcv(self.coins[idx]['symbol'], interval, date_test, 300)
                kandles = Hkac(ohlcv_.ohlcv).kandles
                # p(kandles)
                # kandles = test_data # test data

                df = pd.DataFrame(kandles, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'HKOpen', 'HKHigh', 'HKLow', 'HKClose'])
                # indicators
                rsi_ = talib.RSI(df['Close'], timeperiod = 14)
                rsiMA_ = talib.SMA(rsi_, timeperiod = 14)
                rsi = np.nan_to_num(rsi_.to_numpy())
                rsiMA = np.nan_to_num(rsiMA_.to_numpy())
                # p(datetime.fromtimestamp(df['Time'][-1]/1000), "rsi", rsi[-1], "rsiMA", rsiMA[-1])
                time_ =  datetime.fromtimestamp(np.nan_to_num(df['Time'].to_numpy()[-1])/1000)
                close = np.nan_to_num(df['Close'].to_numpy())
                _open = np.nan_to_num(df['Open'].to_numpy())

                LEFT_BAR = 21
                RIGHT_BAR = 21
                hhs = pivothigh(close, LEFT_BAR, RIGHT_BAR)
                lls = pivotlow(close, LEFT_BAR, RIGHT_BAR)

                # TESTING
                # p(self.coins[idx]['symbol'], time_)
                macds = []
                hists = [0,0]
                isOrderPlaced = False
                
                trades=[]
                entryPrice = 0
                exitPrice = 0
                min_trailing = 0.4 # %
                trailing = min_trailing # %
                enableTrailing = False
                forceExit = False
                side = None
                confirm = True
                liquidation = False
                hh = [0]
                ll = [0]
                INVEST = self.invest
                FEE = 0.04 
                LEVERAGE = 20


                for index in range(len(df['Close'])):
                    if (index < 26):continue
                    # p(df['HKClose'][0:index])
                    # MAIN

                    time_ =  datetime.fromtimestamp(np.nan_to_num(df['Time'][0: index].to_numpy()[-1])/1000)

                    # closes_now = df['HKClose'][0: index] #HK
                    closes_now = df['Close'][0: index]

                    # indicators
                    rsi_ = talib.RSI(closes_now, timeperiod = 14)
                    rsiMA_ = talib.SMA(rsi_, timeperiod = 14)
                    macd, macdsignal, macdhist = talib.MACD(closes_now, fastperiod=12, slowperiod=26, signalperiod=9)

                    # arrays
                    rsi = np.nan_to_num(rsi_.to_numpy())
                    rsiMA = np.nan_to_num(rsiMA_.to_numpy())
                    macd_arr = np.nan_to_num(macd.to_numpy())
                    macdsignal_arr = np.nan_to_num(macdsignal.to_numpy())
                    
                    # Calculating macd 
                    fast_ma_ = talib.EMA(closes_now, 26)
                    slow_ma_ = talib.EMA(closes_now, 14)
                    # macd = fast_ma - slow_ma
                    # hist = macd - signal

                    # arrays
                    fast_ma = np.nan_to_num(fast_ma_.to_numpy())
                    slow_ma = np.nan_to_num(slow_ma_.to_numpy())
                    
                    macd = fast_ma[-1] - slow_ma[-1]
                    macds.append(macd)

                    signal_ = talib.SMA(np.array(macds, dtype=float), 9)
                    hist = macds[-1] - signal_[-1]
                    hists.append(hist)

                    back_length = 100
                    trendHeiht = percentage(min(closes_now[-back_length:]), max(closes_now[-back_length:]))
                    expectedChange = trendHeiht/2 #.50 # trendHeiht/2

                    high = max(closes_now[-back_length:]);
                    low = min(closes_now[-back_length:]);
                    volume = high - low;
                    # perc = (val) => ((high - val) / volume) * 100;

                    # LL
                    if(not np.isnan(lls[index]) and ll[-1] != lls[index]):
                        ll.append(lls[index])
                    # HH
                    if(not np.isnan(hhs[index]) and hh[-1] != hhs[index]):
                        hh.append(hhs[index])
           
                    

                 
                    # if(hists[-1] < hists[-2] and not isOrderPlaced and longSupport and side == None):
                    
                    # ENTRY LONG
             
                    # if((hists[-1] < hists[-2] and not hists[-2] < hists[-3])and not isOrderPlaced):
                    # and macd_arr[-1] > macdsignal_arr[-1]
                    # if(hists[-1] < hists[-2] and not isOrderPlaced and not hists[-2] < hists[-3]):
                    if(hists[-1] < hists[-2] and not isOrderPlaced and not hists[-3] < hists[-4]):
                    # if(hists[-1] < hists[-2] and not isOrderPlaced):
                     
                        p_height = percentage(exitPrice, _open[index-1])
                        # req_4entry_height = -1.5 if liquidation else -0.90 
                        # _open[index-1], close[index-1] 
                        if(-(expectedChange)> p_height or p_height > .10):
                        # if(-(expectedChange) > p_height or len(trades)==0):
                            # print(entryPrice > _open[index])
                            print(f"\n\nPOSITION LONG", time_, f'{expectedChange:.2f}'+'%', "NEXT INVEST", INVEST)if logs else None
                            print("trendHeiht", trendHeiht, ((high - _open[index]) / volume) * 100)if logs else None
                            isOrderPlaced = True
                            side = 'long'
                            entryPrice = _open[index]
                            pass
                        # else: print("--", p_height)

          
                    p_change = percentage(entryPrice, close[index-1]) 
                    isBullishCandle = close[index-1] > _open[index]
                    
                    # EXIT LONG

                    # TRAILING
                    # if(p_change > trailing and isOrderPlaced):
                    #     trailing += 0.1
                    #     enableTrailing = True

                    # if(p_change < trailing-0.1 and enableTrailing and isOrderPlaced):
                    #     # print("TRAILING EXIT:)", p_change, trailing)
                    #     pass
         
                    # breake out
                    breakout = True in (ele > _open[index] for ele in ll[1:])
                    if(breakout):
                        breakout_point  = _open[index]-price_percentage(ll[-1], 0.2)
                        # breakout = True if _open[index] < ele else False
                        # print(time_, breakout_point, _open[index] < breakout_point)
                    # breakout = False


                    if((-trendHeiht*2 > p_change ) and isOrderPlaced):
                        print("STOPLOSS :(", p_change)
                        # if(breakout):
                        #     print("BREAKE OUT :(", ll,  _open[index], breakout_point)
                        #     ll = [0]

                        liquidation = True
                        pass
                    
                    # trailing_exit = (p_change < trailing-0.1 and enableTrailing and isOrderPlaced)
                    # hist_exit = False
                    # if(not hists[-1] < hists[-2]):
                    #     if(p_change < 0):
                    #         hist_exit = False
                    #     elif(p_change > 0.30):
                    #         hist_exit = True


                    # if((not hists[-1] < hists[-2] ) and isOrderPlaced):
                    # if((not hists[-1] < hists[-2] or _open[index] > close[index]) and isOrderPlaced):
                    # if((not hists[-1] < hists[-2] or p_change > 0.20 or _open[index] > close[index])and isOrderPlaced):
                    # if((hist_exit or -0.30 > p_change)and isOrderPlaced):
                    # if((not hists[-1] < hists[-2]) and isOrderPlaced or trailing_exit):
                    # if((p_change < trailing-0.1 and enableTrailing and isOrderPlaced) or (entryPrice > close[index] and isOrderPlaced)):  # is bullish

                    # if((p_change > .50 or liquidation) and isOrderPlaced):
                   
                     
                    lastCandle = len(close) == index+1
                    if(((p_change > expectedChange/3 and close[index] < close[index-1]) or liquidation or lastCandle) and isOrderPlaced): # new

                        # print("test------", _open[index] < breakout_point) if breakout else print(ll)
                    # if((trailing_exit or liquidation) and isOrderPlaced): # new
                        # print('trendHeiht', f'{trendHeiht:.2f}'+'%', f'{p_change:.2f}'+'%')
                        isOrderPlaced = False
                        enableTrailing = False
                        side = None
                        exitPrice =  _open[index] # close[index]
                        trailing = min_trailing
                        liquidation = False

                       


                        amount = INVEST/entryPrice
                        exit_size = amount*exitPrice
                       

                        # LEVERAGE
                        l_amount = amount*LEVERAGE
                        l_entry_size = INVEST*LEVERAGE
                        l_exit_size = exit_size*LEVERAGE

                        amount_entry_fee = price_percentage(l_entry_size, FEE)
                        amount_exit_fee = price_percentage(l_exit_size, FEE)
                        pl = (l_exit_size-l_entry_size)-(amount_entry_fee+amount_exit_fee)

                        # print("ENTRY:", l_entry_size, "EXIT", l_exit_size, "PL:", pl)
                        print("entry:", entryPrice, "exit:",exitPrice,"\nCLOSE POSITION LONG", time_, f'{p_change:.2f}'+'%', "PL:", pl)if logs else None
                        # print("high->", f'{high:.2f}'+'%', "low->", f'{low:.2f}'+'%',)
                        # print("INVEST",self.invest)
                        INVEST = INVEST+pl
                        trades.append(pl)
                       

                        # if( -2 > sum(trades) ):
                        #     break
                        if(sum(trades)>10):
                            INVEST = 10
                      

                # print("\n\n\n\nDAY PL------ ",len(trades), "-->",sum(trades))
                # print(self.coins[idx]['symbol'], "DAY PL------ ",len(trades), "-->",sum(trades))
                day  = INVEST if sum(trades) < -INVEST else sum(trades)
                print(self.dates[idx], "DAY PL------ ",len(trades), "-->",day)
                # self.invest = INVEST+sum(trades)
                # self.invest = 10 if (INVEST+sum(trades))<10 else sum(trades)
                # if(sum(trades)<10):
                #     print("ADDED $10")
                self.month.append(day)
                    
                time.sleep(.1)
                exit()if logs else None
                # if(idx == 0): break # dev

            # end of testing
            print("\n\nMONTH PL-------->",sum(self.month))
            # self.month.clear()
            break



for coin in coins:
    print(coin)  
    bot = Bot(coin, '5m', 10)
    bot.run()
    time.sleep(5)
            

#  MAIN
# bot = Bot({"symbol": "XRP/USDT"}, '5m', 10)
# bot.run()
# bot = Bot({"symbol": "BTT/USDT"}, '5m', 10)
# print(test_data)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(bot.run())

# loop.close()

# UTILS
# def percentage(num1, num2):
#     return 100-((num1/num2)*100)
# print(percentage(0.3366, 0.3369))

# Trailing test
# changes = [0.08, 0.04, 0.12, 0.18, 0.22 ,0.31, 0.35,  0.32, 0.38, 0.41, 0.39]
# min_trailing = 0.2
# trailing = 0.2
# enableTrailing = False
# for ch in changes:
#     print("->", ch, trailing)
#     if(ch > trailing):
#         trailing += 0.1
#         enableTrailing = True

#     if(ch < trailing-0.1 and enableTrailing):
#         print("leave")
#    p_change = percentage(entryPrice, close[index-1]) 
#                     trailing = 0.2
#                     if(p_change > trailing+0.1)
#                         trailing += trailing+0.1


# print(tpsl_price(1000, 2)['tp'], tpsl_price(1000, 1)['sl'])
