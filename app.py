from mqttParser import MQTTParser

mqtt_parser = MQTTParser("fortuitous-welder.cloudmqtt.com", 1883, "CodeJamUser", "123CodeJam", True, 1, "SSHY01", "CodeJam", "/Users/gordon/Desktop/Hackathon/Logs")
mqtt_parser.start()