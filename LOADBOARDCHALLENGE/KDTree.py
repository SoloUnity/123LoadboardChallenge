class KDTree:
    class KDNode:
        def __init__(self, coord, truck_id, truck_type, left=None, right=None, time=None, nextTripPreference=None):
            self.coord = coord  # (latitude, longitude)
            self.truck_id = truck_id
            self.truck_type = truck_type
            self.time = time
            self.nextTripPreference = nextTripPreference
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.truck_map = {}

    def insert(self, coord, truck_id, truck_type):
        if truck_id in self.truck_map:
            truck_node = self.truck_map[truck_id]
            truck_node.coord = coord
            truck_node.truck_type = truck_type
        else:
            self.root = self._insertKDNode(self.root, coord, truck_id, truck_type)
            self.truck_map[truck_id] = self.root

    def _insertKDNode(self, root, coord, truck_id, truck_type, depth=0):
        if root is None:
            return self.KDNode(coord, truck_id, truck_type)

        cd = depth % 2
        if coord[cd] < root.coord[cd]:
            root.left = self._insertKDNode(root.left, coord, truck_id, truck_type, depth + 1)
        else:
            root.right = self._insertKDNode(root.right, coord, truck_id, truck_type, depth + 1)

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

    def findNearestNeighbor(self, target_coord):
        return self._find_nearest_neighbor(self.root, target_coord)

    def _find_nearest_neighbor(self, root, target_coord, depth=0, best=None):
        if root is None:
            return best

        if best is None or self._distance(target_coord, root.coord) < self._distance(target_coord, best.coord):
            best = root

        cd = depth % 2

        if target_coord[cd] < root.coord[cd]:
            best = self._find_nearest_neighbor(root.left, target_coord, depth + 1, best)
            if abs(target_coord[cd] - root.coord[cd]) < self._distance(target_coord, best.coord):
                best = self._find_nearest_neighbor(root.right, target_coord, depth + 1, best)
        else:
            best = self._find_nearest_neighbor(root.right, target_coord, depth + 1, best)
            if abs(target_coord[cd] - root.coord[cd]) < self._distance(target_coord, best.coord):
                best = self._find_nearest_neighbor(root.left, target_coord, depth + 1, best)

        return best

    def _distance(self, coord1, coord2):
        return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5
