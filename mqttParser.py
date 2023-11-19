import paho.mqtt.client as mqtt
import json
from KDTree import KDTree  # Import KDTree class

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
        try:
            data = json.loads(msg.payload.decode())
            msg_type = data.get("type", "Unknown")

            
            if msg_type == "Start":
                print("Start message received at timestamp:", data.get("timestamp"))
            elif msg_type == "End":
                print("End message received at timestamp:", data.get("timestamp"))
                load = {}
                truck = {}
            elif msg_type == "Truck":
                truck_id = data.get("truckID")
                latitude = data.get("positionLatitude")
                longitude = data.get("positionLongitude")
                truck_type = data.get("equipType")
                time = data.get("timestamp")
                nextTripPreference = data.get("nextTripLengthPreference")
                #kdTree.insert((latitude, longitude), truck_id, truck_type, time, nextTripPreference)

                print(f"Truck {str(truck_id)} at position ({latitude}, {longitude})")

            elif msg_type == "Load":
                #load[data.get("loadID")] = (data['timestamp'], data['positionLatitude'], data['positionLongitude'], )
                print(f"Load {data['loadId']} from ({data['originLatitude']}, {data['originLongitude']}) to ({data['destinationLatitude']}, {data['destinationLongitude']})")
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