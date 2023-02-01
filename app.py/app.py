#first reveal yourself publicy -> Connect to drone -> create function that will enable drone to act on vision data --> done

#winch is REST api -> built on https 


import asyncio
import websockets
from flyt_python import API


async def listen_to_data():
    async with websockets.connect("wss://app.flytnow.com:8080/guest/63da97ae26930d0013649752") as websocket:
        while True:
            data = await websocket.recv()
            print(data)

asyncio.run(listen_to_data())
