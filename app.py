#first reveal yourself publicy -> Connect to drone -> create function that will enable drone to act on vision data --> done

#winch is REST api -> built on https 
#API KEY: NjEzZDA4MjI0YjIzYmM0NGJkNjU5ZDlhNzZkZDEzODk4MmYzNzE3OGFiZjc4OWZhMThhYzE5MjQ=

import asyncio
import websockets


async def listen_to_data(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print(data)

asyncio.run(listen_to_data("https://app.flytnow.com/guest/63da97ae26930d0013649752/dashboard"))

#test
