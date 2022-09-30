from time import time
import websockets
import asyncio
import json
import talib
import pandas as pd

from ohlcv import Ohlcv

class Bot:
    cc = 'lunabusd'
    interval = '1m'
    socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'
    numberOfCandles = 50

    kandles = []

    # def __init__(self):
        # pass 

    ohlcv_ = Ohlcv('LUNA/BUSD', interval, 1654083158, numberOfCandles)
    kandles = ohlcv_.ohlcv
    # print(kandles)

        
    async def stream(self):
        async with websockets.connect(self.socket) as websocket:
            while True:
                # await websocket.send("Hello world!")
                last_kandle = await websocket.recv()
                lk_arr = json.loads(last_kandle)
                # print(lk_arr[0])
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

                df = pd.DataFrame(self.kandles, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                rsi = talib.RSI(df['Close'].to_numpy(), timeperiod = 14)
                print(rsi[-1])

                # print(rsi[-1], "Close -> ", df['Close'].to_numpy()[-1])
                if(rsi[-1] > 70):print("SELL")
                if(rsi[-1] < 30):print("BUY")


#  MAIN
bot = Bot()

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.stream())
# loop.run_until_complete(do_other_things())

loop.close()
# asyncio.run(bot.stream())
