import paho.mqtt.client as mqtt
import json
import asyncio
from truckerFindLoads import trucker_find_loads
import websockets
import queue
from KDTreeLoads import KDTree


message_queue = queue.Queue()
#Breaks if we turn it into a class, so we're not gonna touch what works

uri = "ws://localhost:8765"
websocket_connection = None


#TODO: make this so that it does not open and close a connection every time it sends a message

def websocket_thread_func():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        message = message_queue.get()
        asyncio.run(send_to_websocket(message))

async def start_websocket_connection():
    global websocket_connection
    if not websocket_connection or websocket_connection.closed:
        websocket_connection = await websockets.connect(uri)
        print("WebSocket connection established")

async def send_to_websocket(data_to_send):
    async with websockets.connect(uri) as websocket:
        await websocket.send(data_to_send)
        print(f"Sent to server: {data_to_send}")

async def close_websocket_connection():
    global websocket_connection
    if websocket_connection:
        await websocket_connection.close()
        websocket_connection = None
        print("WebSocket connection closed")

def mqttParser(kdTree):
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
        try:
            data = json.loads(msg.payload.decode())
            msg_type = data.get("type", "Unknown")

            if msg_type == "Start":
                print("Start message received at timestamp:", data.get("timestamp"))
                asyncio.create_task(start_websocket_connection())

            elif msg_type == "End":
                print("End message received at timestamp:", data.get("timestamp"))
                asyncio.create_task(close_websocket_connection())
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
                print(trucker_find_loads(kdTree, truck_id, trucks[truck_id]))

                if websocket_connection is not None:
                    asyncio.run(send_to_websocket(msg.payload.decode()))

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

                kdTree.insert_load(origin_latitude, origin_longitude, load_id, load_type, load_details)
                print(f"Load {data['loadId']} from ({data['originLatitude']}, {data['originLongitude']}) to ({data['destinationLatitude']}, {data['destinationLongitude']})")


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
    kdTree = KDTree()

    start_websocket_connection()
    mqttParser(kdTree)

if __name__ == "__main__":
    mqtt_main()