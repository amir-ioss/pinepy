import time
import ccxt, pymongo
import random, json, sys, string, secrets
from typing import Union, List
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
from ConnectionManager import ConnectionManager
import sys 
from multiprocessing import Process
import threading

sys.path.append('..')

from bo import Scalp

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# myclient = pymongo.MongoClient(
#     "mongodb+srv://rd2:ioss@cluster0.xlbfpwk.mongodb.net/?retryWrites=true&w=majority")
# mydb = myclient["tri-arb-bot"]
# collUsers = mydb["users"]
# trades = mydb["trades"]

# @app.get("/")
# def read_root():
#     # x = collUsers.find_one()
#     return "hi.."

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.post("/save_trade")
# async def save_trade(trade: dict):
#     trades.insert_one(trade)
#     print(trade)
#     return {"responce": "Trade add to history"}



# from fastapi.responses import HTMLResponse
# from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status


# @app.get("/ami")
# async def get():
#     return HTMLResponse(html)


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


@app.get("/")
async def get():
    return "Welcome Home"

manager = ConnectionManager()



@app.websocket("/ws_/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    print('a new websocket to create.')
    #await websocket.accept()
    await manager.connect(websocket)

    def callback(val):
        manager.send_personal_message(val, websocket)
        # print("function my_callback was called with ", val)

    try:
        bot = Scalp({"symbol": "TRX/BUSD"}, '1m', 12.22)
        await bot.run(callback)
    except Exception as e:
        print('error:', e)


    # while True:
    #     try:
    #         # Wait for any message from the client
    #         rec = await websocket.receive_text()
    #         print(client_id, rec)
    #         # Send message to the client
    #         resp = {'value': random(0, 1)}
    #         # await websocket.send_json(resp)
    #         # await manager.send_personal_message(resp, websocket)
    #         await manager.send_personal_message(resp, websocket)
    #     except Exception as e:
    #         manager.disconnect(websocket)
    #         await manager.broadcast(f"Client #{client_id} left the chat")
    #         print('error:', e)
    #         break
    # print('Bye..')

# import nest_asyncio
# nest_asyncio.apply()
# __import__('IPython').embed()




@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # await websocket.accept()
    # msg = {'name': 'amir'}

  
    bot = Scalp(manager, websocket, {"symbol": "TRX/BUSD"}, '1m', 12.22)
    await bot.run()
    # bot = Test(manager, websocket)
    # await bot.run()
    # await bot.chart()

    # test1 = threading.Thread(target=bot.run, args=(None))
    # test2 = threading.Thread(target=bot.chart, args=(None))
    
    # test1.start()    
    # test2.start() 

    # test1.join()
	# test2.join()
    

   


class Test:
    def __init__(self, manager, websocket):
        self.socket = websocket
        self.manager = manager
        # self.chart = "NO CAHRT"
        pass

    async def run(self,):
        print("BOT CREATED")
        # await self.socket.accept()
        await self.manager.connect(self.socket)

        while True:
            try:
                # time.sleep(1)
                print("--")
                # await self.chart()
                # self.chart = str(random(0, 1)) 
                await self.manager.sendText(str(random.uniform(0, 1)), self.socket)               
            except Exception as e:
                # self.socket.disconnect(self.socket)
                self.manager.disconnect(self.socket)
                print('error:', e)
                break
        pass


    async def chart(self,):
        print("ON_CHART")
        # await self.socket.accept()
        await self.manager.connect(self.socket)
        while True:
            try:
                # await self.socket.send_text(str(random(0, 1)))
                await self.manager.send_personal_message(str(random(0, 1)), self.socket)
                
            except Exception as e:
                # self.socket.disconnect(self.socket)
                self.manager.disconnect(self.socket)
                print('error:', e)
                break
        pass

# ps -fA | grep python
# kill -9 pid


