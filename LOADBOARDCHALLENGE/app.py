from mqttParser import mqttParser
from KDTreeLoads import KDTree
#from pushNotification import send_notification

FROM_NUMBER = "+16562188280"
global kdTree
global kdTreeShort
kdTreeLong = KDTree()
kdTreeShort = KDTree()
mqttParser(kdTreeLong, kdTreeShort)

# if __name__ == "__main__":
#     send_notification("Hello world", FROM_NUMBER, "+14384091737")
