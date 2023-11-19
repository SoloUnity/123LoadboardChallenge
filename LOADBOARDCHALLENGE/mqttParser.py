import paho.mqtt.client as mqtt
import json
from truckerFindLoads import trucker_find_loads
import queue
import time
import threading
#Breaks if we turn it into a class, so we're not gonna touch what works


def mqttParser(kdTreeLong, kdTreeShort):
    # MQTT connection details
    host = "fortuitous-welder.cloudmqtt.com"
    port = 1883  # non SSL port
    username = "CodeJamUser"
    password = "123CodeJam"

    # Additional settings
    clean_session = True
    qos = 1
    client_id = "SSHY01" 
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
        try:
            data = json.loads(msg.payload.decode())
            msg_type = data.get("type", "Unknown")

            
            if msg_type == "Start":
                print("Start message received at timestamp:", data.get("timestamp"))

            elif msg_type == "End":
                print("End message received at timestamp:", data.get("timestamp"))
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
                load_info = trucker_find_loads(kdTreeLong, kdTreeShort, truck_id, trucks[truck_id])
                print(load_info)
                if load_info[2] == "negative profit":
            # Put the truck back in the queue for later processing
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
    
    
    
