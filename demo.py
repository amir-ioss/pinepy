from random import random
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import socket
from server.ConnectionManager import ConnectionManager
from websocket import create_connection

# manager = ConnectionManager()

# async def test(websocket: WebSocket):
#     await manager.connect(websocket)
#     resp = {'value': "Amir Abbasy"}
#     await manager.send_personal_message(f"You wrote: {resp}", websocket)


# # run
# test(WebSocket)


import json

params = {}
params['Type'] = "Admin"
params['Request'] = 'Login'
params['RequestId'] = 1
params['Params'] = {'AuthTag': 'user-admin',
                     'Password': '211fdd69b8942c10cef6cfb8a4748fa4' }


def client_program():
    ws = create_connection("ws://127.0.0.1:8000/ws/ami")
    # print(ws)
    ws.send("hi")

    # try:
    #     ws.send(json.dumps(params))
    # except Exception as e:
    #     print(e)
                
    # socket.send(JSON.stringify(temp1);
    # ws.send(json.dumps([json.dumps({'msg': 'connect', 'version': '1', 'support': ['1', 'pre2', 'pre1']})]))
    # print "Sent"
    # print "Receiving..."
    # result =  ws.recv()
    # print('Result: {}'.format(result))
    ws.close()

client_program()