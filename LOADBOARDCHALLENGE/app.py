import asyncio
from websockets.server import serve
import websockets

connected = set()

async def echo(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            for client in connected:
                if client != websocket and not client.closed:  # Check if client is not closed
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        # Handle individual client disconnections
                        connected.remove(client)
                        print(f"WebSocket connection closed with {client.remote_address}")
    except websockets.exceptions.ConnectionClosed:
        # Handle disconnection of the client in the current iteration
        print(f"WebSocket connection closed with {websocket.remote_address}")
    finally:
        connected.remove(websocket)
        print(f"WebSocket connection closed with {websocket.remote_address}")

async def start_websocket_server():
    async with serve(echo, "localhost", 8765):
        print("WebSocket server is running on ws://localhost:8765")
        try:
            await asyncio.Future() 
        except asyncio.CancelledError:
            print("Server shutdown initiated, closing connections...")

async def run_app():
    try:
        await start_websocket_server()
    except KeyboardInterrupt:
        print("Program interrupted, shutting down...")

if __name__ == "__main__":
    asyncio.run(run_app())