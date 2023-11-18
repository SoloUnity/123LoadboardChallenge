import paho.mqtt.client as mqtt
import json
from truckerFindLoads import trucker_find_loads
#Breaks if we turn it into a class, so we're not gonna touch what works


def mqttParser(kdTree):
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
                    "point": (latitude,longitude),
                    "truck_type": truck_type,
                    "time": time,
                    "next_trip_preference": next_trip_preference,
                    "past_loads": []
                }
                print("---------------------------------------------------------------------------")
                print(truck_id)
                print(trucker_find_loads(kdTree, trucks[truck_id]))


            elif msg_type == "Load":
                load_id = data.get("loadId")
                time = data['timestamp']
                load_type = data['equipmentType']
                origin_latitude = data['originLatitude']
                origin_longitude = data['originLongitude']
                dest_point = (data['destinationLatitude'],data['destinationLongitude'])
                mileage = data['mileage']
                price = data['price']


                kdTree.insert_load(origin_latitude, origin_longitude, load_id, load_type, time, mileage, price, dest_point)
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