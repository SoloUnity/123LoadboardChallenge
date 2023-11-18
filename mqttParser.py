import paho.mqtt.client as mqtt
import time
import os
import json

class MQTTParser:

    def __init__(self, host, port, username, password, clean_session, qos, client_id, topic, log_directory):
        # MQTT connection details
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        # Additional settings
        self.clean_session = clean_session
        self.qos = qos
        self.client_id = client_id
        self.topic = topic

        # Directory to save JSON files
        self.log_directory = log_directory

        # Ensure the directory exists
        os.makedirs(self.log_directory, exist_ok=True)

        # Initialize the MQTT client
        self.client = mqtt.Client(self.client_id, clean_session=self.clean_session)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # Callback when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            self.client.subscribe(self.topic, qos=self.qos)
        else:
            print("Connection failed with code", rc)

    # Callback when a message is received from the server.
    def on_message(self, client, userdata, msg):
        message_data = {
            "topic": msg.topic,
            "message": msg.payload.decode(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Construct the file name with timestamp
        filename = f"mqtt_message_{int(time.time())}.json"
        file_path = os.path.join(self.log_directory, filename)

        # Save the message data to a JSON file
        with open(file_path, "w") as file:
            json.dump(message_data, file, indent=4)

        print(f"Message saved to {filename}")

    def start(self):
        # Connect to the MQTT broker and start the loop
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

mqtt_parser = MQTTParser("fortuitous-welder.cloudmqtt.com", 1883, "CodeJamUser", "123CodeJam", True, 1, "SSHY01", "CodeJam", "/Users/gordon/Desktop/Hackathon/Logs")
mqtt_parser.start()

