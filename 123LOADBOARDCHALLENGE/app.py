from mqttParser import mqttParser
from KDTree import KDTree
from pushNotification import send_notification

FROM_NUMBER = "+16562188280"

# kdTree = KDTree()

# mqttParser.mqttParser(kdTree)

if __name__ == "__main__":
    send_notification("Hello world", FROM_NUMBER, "+14384091737")
