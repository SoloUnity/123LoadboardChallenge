class KDNode:
    def __init__(self, point, truck_id, truck_type, left=None, right=None):
        self.point = point  # (latitude, longitude)
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

def addOrUpdateTruck(truck_map, truck_tree, truck_id, point, truck_type):
    if truck_id in truck_map:
        # Update existing truck's info
        truck_node = truck_map[truck_id]
        truck_node.point = point
        truck_node.truck_type = truck_type
    else:
        # Insert new truck
        new_tree = insertKDNode(truck_tree, point, truck_id, truck_type)
        truck_map[truck_id] = new_tree
        return new_tree
    return truck_tree

def getTruckByID(truck_map, truck_id):
    return truck_map.get(truck_id)

def getTrucksByType(root, truck_type):
    if root is None:
        return []

    trucks = []
    if root.truck_type == truck_type:
        trucks.append(root)

    trucks += getTrucksByType(root.left, truck_type)
    trucks += getTrucksByType(root.right, truck_type)

    return trucks

def find_nearest_neighbor(root, target_point, depth=0, best=None):
    if root is None:
        return best

    if best is None or distance(target_point, root.point) < distance(target_point, best.point):
        best = root

    cd = depth % 2

    if target_point[cd] < root.point[cd]:
        best = find_nearest_neighbor(root.left, target_point, depth + 1, best)
        if abs(target_point[cd] - root.point[cd]) < distance(target_point, best.point):
            best = find_nearest_neighbor(root.right, target_point, depth + 1, best)
    else:
        best = find_nearest_neighbor(root.right, target_point, depth + 1, best)
        if abs(target_point[cd] - root.point[cd]) < distance(target_point, best.point):
            best = find_nearest_neighbor(root.left, target_point, depth + 1, best)

    return best

def distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
