
from datetime import datetime
from time import sleep
from ohlcv import Ohlcv
import talib
import asyncio
import json
import calendar
import pandas as pd
import client
from log import p 
from markets import markets
import websockets

class Bot:

    def __init__(self, coin):
        interval = '1m'
        numberOfCandles = 205
        self.coin = coin

        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())
        since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds
        # start_dt = datetime.fromtimestamp(ohlcv[0][0]/1000)

        ohlcv_ = Ohlcv(self.coin["symbol"], interval, None, numberOfCandles)
        # ohlcv_ = Ohlcv("DEGO/USDT", interval, None, numberOfCandles)
        self.kandles = ohlcv_.ohlcv
        # print(kandles)

        # ignore stable coins
        # stableRate = 0
        # for idx, item in enumerate(self.kandles):
        #     # p(idx, item, self.kandles[idx-4]) 
        #     if stableRate > 3:
        #         return
        #     if idx < 5 : continue;
        #     if item[4] == self.kandles[idx-1][4]:
        #         stableRate += 1
        #     else : stableRate = 0

        self.df = pd.DataFrame(self.kandles, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        self.rsi = talib.RSI(self.df['Close'].to_numpy(), timeperiod = 14)
        self.ma = talib.MA(self.df['Close'].to_numpy(), timeperiod=200, matype=0)
        self.color = "~GREEN" if self.ma[-1] > self.df['Close'].to_numpy()[-1] else "~RED"
        p(self.coin['symbol'], "[RSI]", self.rsi[-1])


    def run(self):
         if self.rsi[-1] < 30 and self.rsi[-1] != 0 and self.ma[-1] < self.df['Close'].to_numpy()[-1]: 
            p(self.coin['symbol'], "[RSI]", self.rsi[-1], self.color, "[MA-200]", self.ma[-1], "[Close]", self.df['Close'].to_numpy()[-1])
            return self.coin['symbol']

    async def stream(self):
        cc = self.coin["lowercaseId"]
        interval = '1m'
        socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'
        isPlacedOrder = False
        buyPrice = 0
        isCompleted = False

        async with websockets.connect(socket) as websocket:
            while not isCompleted:
                # await websocket.send("Hello world!")
                last_kandle = await websocket.recv()
                lk_arr = json.loads(last_kandle)
                new_candle = [
                lk_arr["k"]["t"],
                float(lk_arr["k"]["o"]), 
                float(lk_arr["k"]["h"]),
                float(lk_arr["k"]["l"]),
                float(lk_arr["k"]["c"]),
                float(lk_arr["k"]["v"])
                ]
                self.kandles.append(new_candle)
                self.kandles.pop(0)
                # print(lk_arr["k"]["c"])

                self.rsi = talib.RSI(self.df['Close'].to_numpy(), timeperiod = 14)
                print(self.rsi[-1])
                if buyPrice == 0: buyPrice = self.df['Close'].to_numpy()[-1]
                
                # if(self.rsi[-1] < 20):p("BUY",  df['Close'].to_numpy()[-1])
                if(self.rsi[-1] > 70):
                    p("SELL",  self.df['Close'].to_numpy()[-1])
                    
                    invest = 12
                    amount = invest/buyPrice
                    priceDiff = self.df['Close'].to_numpy()[-1] - buyPrice
                    profit = amount*priceDiff

                    file1 = open("logs.txt", "a")
                    L = [f"\n{self.coin['symbol']} buy:{buyPrice} sell:{self.df['Close'].to_numpy()[-1]}\nProfit : $ {profit}\nProfit Inr : {profit*76}\nTime:{self.df['Time'].to_numpy()[-1]}\n"]
                    file1.writelines(L)
                    file1.close()
                    isCompleted = True
                    return True



#  MAIN
# bot = Bot()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(bot.stream())
# loop.run_until_complete(do_other_things())

# loop.close()
# asyncio.run(bot.stream())


def start():
    for item in client.markets:
        # print(item['symbol'].split("/")[1] == "USDT")
        filterCoin = item['symbol'].split("/")[1] == "USDT" and item["info"]["status"] == "TRADING" and item['symbol'] in markets
        if filterCoin:
            bot = Bot(item)
            data = bot.run()
            if data:
                done = asyncio.run(bot.stream())
                p(item['symbol'], "==============", done)
                if done: start()
                break;

    sleep(60)
    p("sleep...")            
    start()
    # end start fun


# bot.run()
start()

# for item in json.load(markets):
#     bot = Bot(item)


