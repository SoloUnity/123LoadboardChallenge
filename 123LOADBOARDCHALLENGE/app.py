from mqttParser import mqttParser
from KDTreeLoads import KDTree
import asyncio

kdTree = KDTree()

mqttParser(kdTree)
