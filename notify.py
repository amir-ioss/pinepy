import asyncio
from datetime import datetime
import time
from ohlcv import Ohlcv
from hkac import Hkac
import calendar
from str_rsi import str_rsi 
from order import order 
import requests

import talib
import json
import pandas as pd
import numpy as np
from log import p 



def sendPhoto(symbol = "TRX/USDT", type="BUY", rsi = 0, price= 0, time =""):
    token = "5698404405:AAEOBfZb2M2Y-FknR1jL7PpDU-1rZiMIDR8"
    # method = "sendMessage" # text
    method = "sendPhoto" # caption
    # iconImage = "https://cryptoicons.org/api/icon/{0}/500".format(symbol.split("/")[0].lower())
    iconImage =  "https://coinicons-api.vercel.app/api/icon/"+symbol.split("/")[0].lower()
    indic = "🍏" if type == "BUY" else "🍎" 
    message = indic+" {0}\nRSI Indicator {1} \nPrice: {2}\nOn: {3}".format(symbol, rsi, price, time)
    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            data={'chat_id': 851589325, 'caption': message, "photo": iconImage,  "parseMode": "ParseMode.Html"}
        ).json()
    # print(response)
    pass



class Scan:
    def __init__(self):
        self.count = 0
        self.oneTimeRun = False
        self.coins =[
        {"symbol": "LUNC/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "BTC/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "ETH/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "ADA/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "BNB/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "MATIC/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "SOL/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "DOGE/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "LTC/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "TRX/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "DOT/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        },{
        "symbol": "AVAX/USDT",
         "placeOrder" : False,
         "rsiBelow": False
        }
        ]
        pass

    async def run(self,):
        while True:
            # p("\n                         ---- scanning  ----\n")
            p('                                           scanning...')

            # for each coin 
            for idx in range(len(self.coins)):
                # p("ON", self.coins[idx]['symbol'])

                interval = '15m'
                now = datetime.utcnow()
                unixtime = calendar.timegm(now.utctimetuple())
                since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
                # start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)

                ohlcv_ = Ohlcv(self.coins[idx]['symbol'], interval, None, 50)
                # ohlcv_ = Ohlcv("DEGO/USDT", interval, since, numberOfCandles)
                kandles = Hkac(ohlcv_.ohlcv).kandles
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
                # set rsi conformation
                if(rsi[-1] < 30 ):
                    self.coins[idx]['rsiBelow'] = True
                
                if(rsi[-1] > rsi[-2] and self.coins[idx]['rsiBelow'] == True and self.coins[idx]['placeOrder'] == False):
                    # wait for crossover ma
                    # p("YES")
                    if(rsi[-1] > rsiMA[-1] and rsiMA[-1] > rsiMA[-2]):
                        self.coins[idx]['placeOrder'] = True
                        # notify buy
                        sendPhoto(symbol=self.coins[idx]['symbol'], type="BUY", rsi=rsi[-1], price=close[-1], time=time_)
                        p("ON", self.coins[idx]['symbol'], time_, "|||||| BUY  ||||||\n", self.coins[idx]['symbol'])
                else: 
                    # p("NO")
                    if(rsi[-1] < rsiMA[-1] and self.coins[idx]['placeOrder'] == True):
                        self.coins[idx]['placeOrder'] = False
                        self.coins[idx]['rsiBelow'] == False
                        # notify sell
                        sendPhoto(symbol=self.coins[idx]['symbol'], type="SELL", rsi=rsi[-1], price=close[-1], time=time_)
                        p("ON", self.coins[idx]['symbol'], time_," <<<<  SELL  >>>>\n", self.coins[idx]['symbol'])
                        p("")



                    # p(self.coins[idx])

                time.sleep(900/len(self.coins)) # wait 5 seconds
                # p("")


                # testing
                # for index in range(len(df['HKClose'])):
                #     if (index < 15):continue
                #     # p(df['HKClose'][0:index])
                #     # MAIN

                #       # indicators
                #     rsi_ = talib.RSI(df['HKClose'][0: index], timeperiod = 14)
                #     rsiMA_ = talib.SMA(rsi_, timeperiod = 14)
                #     rsi = np.nan_to_num(rsi_.to_numpy())
                #     rsiMA = np.nan_to_num(rsiMA_.to_numpy())
                #     # p("rsi", rsi[-1], "rsiMA", rsiMA[-1])

                #     if(rsi[-1] < 30 and self.coins[idx]['rsiBelow'] == False):
                #         self.coins[idx]['rsiBelow'] = True
                #         pass
                    
                #     if(rsi[-1] > rsi[-2] and self.coins[idx]['rsiBelow'] == True and self.coins[idx]['placeOrder'] == False):
                #         p("YES")
                #         if(rsi[-1] > rsiMA[-1]):
                #             self.coins[idx]['placeOrder'] = True
                #             # notify buy
                #             p("|||||| BUY  ||||||", self.coins[idx]['symbol'])
                #     else: 
                #         # p("NO")
                #         p("")
                #         if(rsi[-1] < rsiMA[-1] and self.coins[idx]['placeOrder'] == True):
                #             self.coins[idx]['placeOrder'] = False
                #             self.coins[idx]['rsiBelow'] == False
                #             # notify sell
                #             p("|||||| SELL  ||||||", self.coins[idx]['symbol'])
                # time.sleep(60)
                # if(idx == 0): break

            # end of testing
            
            

#  MAIN
bot = Scan()
# bot = Scalp({"symbol": "LUNC/USDT"}, '1m', 12.22)

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run())

# loop.close()
