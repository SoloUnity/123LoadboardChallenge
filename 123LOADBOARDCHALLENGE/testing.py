import asyncio
import websockets

async def test():
    uri = "wss://0365-142-117-215-213.ngrok.io"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server!")
        while True:  # Keep the connection open to listen for messages
            response = await websocket.recv()
            print(f"Received from server: {response}")

asyncio.get_event_loop().run_until_complete(test())