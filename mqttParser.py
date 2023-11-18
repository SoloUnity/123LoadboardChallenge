import paho.mqtt.client as mqtt
import json
import time
import os

# MQTT connection details
host = "fortuitous-welder.cloudmqtt.com"
port = 1883  # non SSL port
username = "CodeJamUser"
password = "123CodeJam"

# Additional settings
clean_session = True
qos = 1
client_id = "SSHY01"  # Replace <team name> with your team name
topic = "CodeJam"

# Directory to save JSON files
log_directory = "/Users/gordon/Desktop/Hackathon/Logs"

# Ensure the directory exists
os.makedirs(log_directory, exist_ok=True)

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(topic, qos=qos)
    else:
        print("Connection failed with code", rc)

# Callback when a message is received from the server.
def on_message(client, userdata, msg):
    # Construct the file name with timestamp
    filename = f"mqtt_message_{int(time.time())}.json"
    file_path = os.path.join(log_directory, filename)

    # Write the message payload directly to a file
    with open(file_path, "wb") as file:
        file.write(msg.payload)

    print(f"Message saved to {filename}")

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
