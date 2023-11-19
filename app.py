import asyncio
from websockets.server import serve

connected = set()

async def echo(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            for client in connected:
                if client != websocket:  # Optional: prevent sending message back to sender
                    await client.send(message)
    finally:
        connected.remove(websocket)
        print(f"WebSocket connection closed with {websocket.remote_address}")

async def start_websocket_server():
    async with serve(echo, "localhost", 8765):
        print("WebSocket server is running on ws://localhost:8765")
        await asyncio.Future()  # This will keep the server running indefinitely

async def run_app():
    # Start the WebSocket server
    await start_websocket_server()

if __name__ == "__main__":
    asyncio.run(run_app())