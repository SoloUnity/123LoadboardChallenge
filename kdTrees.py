class KDTree:
    class KDNode:
        def __init__(self, point, truck_id, truck_type, left=None, right=None):
            self.point = point  # (latitude, longitude)
            self.truck_id = truck_id
            self.truck_type = truck_type
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.truck_map = {}

    def insert(self, point, truck_id, truck_type):
        if truck_id in self.truck_map:
            truck_node = self.truck_map[truck_id]
            truck_node.point = point
            truck_node.truck_type = truck_type
        else:
            self.root = self._insertKDNode(self.root, point, truck_id, truck_type)
            self.truck_map[truck_id] = self.root

    def _insertKDNode(self, root, point, truck_id, truck_type, depth=0):
        if root is None:
            return self.KDNode(point, truck_id, truck_type)

        cd = depth % 2
        if point[cd] < root.point[cd]:
            root.left = self._insertKDNode(root.left, point, truck_id, truck_type, depth + 1)
        else:
            root.right = self._insertKDNode(root.right, point, truck_id, truck_type, depth + 1)

        return root

    def getTruckByID(self, truck_id):
        return self.truck_map.get(truck_id)

    def getTrucksByType(self, truck_type):
        return self._getTrucksByType(self.root, truck_type)

    def _getTrucksByType(self, root, truck_type):
        if root is None:
            return []

        trucks = []
        if root.truck_type == truck_type:
            trucks.append(root)

        trucks += self._getTrucksByType(root.left, truck_type)
        trucks += self._getTrucksByType(root.right, truck_type)

        return trucks

    def findNearestNeighbor(self, target_point):
        return self._find_nearest_neighbor(self.root, target_point)

    def _find_nearest_neighbor(self, root, target_point, depth=0, best=None):
        if root is None:
            return best

        if best is None or self._distance(target_point, root.point) < self._distance(target_point, best.point):
            best = root

        cd = depth % 2

        if target_point[cd] < root.point[cd]:
            best = self._find_nearest_neighbor(root.left, target_point, depth + 1, best)
            if abs(target_point[cd] - root.point[cd]) < self._distance(target_point, best.point):
                best = self._find_nearest_neighbor(root.right, target_point, depth + 1, best)
        else:
            best = self._find_nearest_neighbor(root.right, target_point, depth + 1, best)
            if abs(target_point[cd] - root.point[cd]) < self._distance(target_point, best.point):
                best = self._find_nearest_neighbor(root.left, target_point, depth + 1, best)

        return best

    def _distance(self, point1, point2):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
