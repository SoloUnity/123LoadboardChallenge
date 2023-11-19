import os
from twilio.rest import Client
import asyncio
from websockets.server import serve

connected = set()

async def echo(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            for client in connected:
                await client.send(message)
    finally:
        connected.remove(websocket)
        print(f"WebSocket connection closed with {websocket.remote_address}")


async def main():
  async with serve(echo, "localhost", 8765):
    print("WebSocket server is running on ws://localhost:8765")
    await asyncio.Future()
      

def send_notification(body, from_, to_):
  account_sid = os.environ['TWILIO_ACCOUNT_SID']
  auth_token = os.environ['TWILIO_AUTH_TOKEN']
  client = Client(account_sid, auth_token)
  
  message = client.messages \
    .create( body=body, from_=from_, to=to_ )
    
  return message.sid

if __name__ == "__main__":
 asyncio.run(main())