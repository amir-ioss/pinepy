import websockets
import asyncio
import json


cc = 'lunabusd'
interval = '5m'
socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'
    
async def stream():
   async with websockets.connect(socket) as websocket:
        while True:
            # await websocket.send("Hello world!")
            kandles = await websocket.recv()
            # print(kandles)
            y = json.loads(kandles)
            # k = json.load(kandles)
            print(y["k"]["c"])
        # async for messages in websocket:
            # print(type(messages))


asyncio.run(stream())
    # await asyncio.sleep(1)


# asyncio.run(hello())



# {"e":"kline","E":1653995532762,"s":"BTCUSDT","k":{"t":1653995400000,"T":1653995699999,"s":"BTCUSDT","i":"5m","f":1387093965,"L":1387095760,"o":"31786.77000000","c":"31739.25000000","h":"31796.66000000","l":"31735.23000000","v":"75.56642000","n":1796,"x":false,"q":"2401211.12482620","V":"33.95945000","Q":"1079206.84279030","B":"0"}}
