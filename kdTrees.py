class KDNode:
    def __init__(self, point, truck_id, truck_type, left=None, right=None):
        self.point = point  # The point (latitude, longitude)
        self.truck_id = truck_id
        self.truck_type = truck_type
        self.left = left
        self.right = right

def insertKDNode(root, point, truck_id, truck_type, depth=0):
    if root is None:
        return KDNode(point, truck_id, truck_type)

    cd = depth % 2

    if point[cd] < root.point[cd]:
        root.left = insertKDNode(root.left, point, truck_id, truck_type, depth + 1)
    else:
        root.right = insertKDNode(root.right, point, truck_id, truck_type, depth + 1)

    return root

truck_map = {}

def addOrUpdateTruck(truck_id, point, truck_type):
    global truck_tree, truck_map
    truck_tree = insertKDNode(truck_tree, point, truck_id, truck_type)
    truck_map[truck_id] = truck_tree

def getTruckByID(truck_id):
    return truck_map.get(truck_id)

def getTrucksByType(root, truck_type, trucks=[]):
    if root is None:
        return trucks

    if root.truck_type == truck_type:
        trucks.append(root)

    trucks = getTrucksByType(root.left, truck_type, trucks)
    trucks = getTrucksByType(root.right, truck_type, trucks)

    return trucks
