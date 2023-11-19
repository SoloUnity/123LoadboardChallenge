import paho.mqtt.client as mqtt
import json
import asyncio
from truckerFindLoads import trucker_find_loads
import websockets
import queue
from KDTreeLoads import KDTree
import threading
import time

message_queue = queue.Queue()
uri = "ws://localhost:8765"
websocket_connection = None
start_event_received = False

async def websocket_thread_func():
    global websocket_connection, start_event_received
    while True:
        try:
            if not websocket_connection or websocket_connection.closed:
                websocket_connection = await websockets.connect(uri)
                print("WebSocket connection established")

            # Check if start event is received before sending messages
            if start_event_received:
                message = await asyncio.to_thread(message_queue.get)
                if websocket_connection and not websocket_connection.closed:
                    await websocket_connection.send(message)
                    print(f"Sent to server: {message}")
                else:
                    print("WebSocket connection is not available")
            else:
                await asyncio.sleep(1)  # Wait and check again

        except websockets.ConnectionClosedError as e:
            print(f"WebSocket connection closed unexpectedly: {e}")
            websocket_connection = None
            await asyncio.sleep(1)  # Wait before attempting to reconnect

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def run_websocket_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_thread_func())

async def start_websocket_connection():
    global websocket_connection
    if not websocket_connection or websocket_connection.closed:
        websocket_connection = await websockets.connect(uri)
        print("WebSocket connection established")

def send_to_websocket(data_to_send):
    loop = asyncio.get_event_loop()
    loop.create_task(_send_to_websocket(data_to_send))

async def _send_to_websocket(data_to_send):
    global websocket_connection
    if websocket_connection and not websocket_connection.closed:
        await websocket_connection.send(data_to_send)
        print(f"Sent to server: {data_to_send}")
    else:
        print("WebSocket connection is not available")

async def close_websocket_connection():
    global websocket_connection
    if websocket_connection:
        await websocket_connection.close()
        websocket_connection = None
        print("WebSocket connection closed")

def mqttParser(kdTreeLong, kdTreeShort):
    global start_event_received

    # MQTT connection details
    host = "fortuitous-welder.cloudmqtt.com"
    port = 1883  # non SSL port
    username = "CodeJamUser"
    password = "123CodeJam"

    # Additional settings
    clean_session = True
    qos = 1
    client_id = "SSHY03"
    topic = "CodeJam"

    trucks = dict()
    loads = dict()
    waiting_queue = queue.Queue()

    def check_waiting_queue():
        while True:
            if not waiting_queue.empty():
                truck_id = waiting_queue.get()
                result = trucker_find_loads(kdTreeLong, kdTreeShort, truck_id, trucks[truck_id])
                
                if result[2] != "negative profit":
                    print(f"Update: Driver {truck_id} found a new load: {result}")
                else:
                    waiting_queue.put(truck_id)

            time.sleep(10)  # Adjust the sleep interval as needed

    check_queue_thread = threading.Thread(target=check_waiting_queue)
    check_queue_thread.daemon = True  # The thread will exit when the main program exits
    check_queue_thread.start()

    # Callback when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            # Subscribe to the topic here if needed
            client.subscribe(topic, qos=qos)
        else:
            print("Connection failed with code", rc)

    # Callback when a message is received from the server.
    def on_message(client, userdata, msg):
        nonlocal trucks, loads
        global start_event_received

        try:
            data = json.loads(msg.payload.decode())
            msg_type = data.get("type", "Unknown")

            
            if msg_type == "Start":
                print("Start message received at timestamp:", data.get("timestamp"))
                start_event_received = True
                asyncio.run_coroutine_threadsafe(start_websocket_connection(), asyncio.get_event_loop())

            elif msg_type == "End":
                print("End message received at timestamp:", data.get("timestamp"))
                start_event_received = False
                # asyncio.run_coroutine_threadsafe(close_websocket_connection(), asyncio.get_event_loop())
                trucks = {}
                loads = {}

            elif msg_type == "Truck":
                
                truck_id = data.get("truckId")
                latitude = data['positionLatitude']
                longitude = data['positionLongitude']
                truck_type = data["equipType"]
                time = data["timestamp"]
                next_trip_preference = data["nextTripLengthPreference"]
                # if truck_id not in trucks:
                #     print(f"Truck {truck_id} at position ({latitude}, {longitude})")

                trucks[truck_id] = {
                    "coords": (latitude,longitude),
                    "truck_type": truck_type,
                    "time": time,
                    "next_trip_preference": next_trip_preference,
                    "past_loads": []
                }
                print("---------------------------------------------------------------------------")
                print(truck_id)
                print(data.get("seq"))
                if start_event_received:
                    load_info = trucker_find_loads(kdTreeLong, kdTreeShort, truck_id, trucks[truck_id])
                    print(load_info)
                    if load_info[2] == "negative profit":
                        waiting_queue.put(truck_id)


            elif msg_type == "Load":
                load_id = data.get("loadId")

                load_type = data['equipmentType']
                origin_latitude = data['originLatitude']
                origin_longitude = data['originLongitude']
                load_details = {
                    'time' : data['timestamp'],
                    'dest_coords' : (data['destinationLatitude'],data['destinationLongitude']),
                    'mileage' : data['mileage'],
                    'price' : data['price']
                }
                if data['mileage'] < 200:
                    kdTreeShort.insert_load(origin_latitude, origin_longitude, load_id, load_type, load_details)
                else:
                    kdTreeLong.insert_load(origin_latitude, origin_longitude, load_id, load_type, load_details)
                #print(f"Load {data['loadId']} from ({data['originLatitude']}, {data['originLongitude']}) to ({data['destinationLatitude']}, {data['destinationLongitude']})")
            else:
                print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

            message_queue.put(msg.payload.decode())

        except json.JSONDecodeError:
            print("Invalid JSON received:", msg.payload.decode())

    # Create an MQTT client instance
    client = mqtt.Client(client_id, clean_session=clean_session)

    # Set username and password
    client.username_pw_set(username, password)

    # Assign the callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(host, port, 60)

    # Start the network loop
    client.loop_forever()

def mqtt_main():
    global kdTree
    global kdTreeShort
    kdTreeLong = KDTree()
    kdTreeShort = KDTree()
    mqttParser(kdTreeLong, kdTreeShort)

if __name__ == "__main__":
    websocket_thread = threading.Thread(target=run_websocket_thread, daemon=True)
    websocket_thread.start()
    mqtt_main()