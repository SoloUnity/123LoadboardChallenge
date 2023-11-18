class KDTree:
    class KDNode:
        def __init__(self, point, load_id, load_type, time=None, mileage=None, price=None, dest_point=None, left=None, right=None):
            self.point = point  # (latitude, longitude)
            self.load_id = load_id
            self.load_type = load_type
            self.time = time
            self.mileage = mileage
            self.price = price
            self.dest_point = dest_point
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.load_map = {}

    def insert_load(self, origin_latitude, origin_longitude, load_id, load_type, time=None, mileage=None, price=None, dest_point=None):
        point = (origin_latitude, origin_longitude)

        if load_id in self.load_map:
            load_node = self.load_map[load_id]
            load_node.point = point
            load_node.load_type = load_type
            load_node.time = time
            load_node.mileage = mileage
            load_node.price = price
            load_node.dest_point = dest_point
        else:
            self.root = self._insertKDNode(self.root, point, load_id, load_type, time, mileage, price, dest_point)
            self.load_map[load_id] = self.root

    def get_load_by_id(self, load_id):
        return self.load_map.get(load_id)

    def find_k_closest_loads(self, target_point, k=5):
        closest_loads = []
        self._find_k_closest_loads(self.root, target_point, closest_loads, k)
        return closest_loads

    def _find_k_closest_loads(self, root, target_point, closest_loads, k, depth=0):
        if root is None:
            return

        distance = self._distance(target_point, root.point)

        if len(closest_loads) < k:
            closest_loads.append((-distance, root))
        elif distance < -closest_loads[0][0]:
            closest_loads[0] = (-distance, root)
        
        closest_loads.sort(key=lambda x: x[0], reverse=True)  # Sort by distance in descending order

        cd = depth % 2

        if target_point[cd] < root.point[cd]:
            self._find_k_closest_loads(root.left, target_point, closest_loads, k, depth + 1)
            if abs(target_point[cd] - root.point[cd]) < -closest_loads[0][0]:
                self._find_k_closest_loads(root.right, target_point, closest_loads, k, depth + 1)
        else:
            self._find_k_closest_loads(root.right, target_point, closest_loads, k, depth + 1)
            if abs(target_point[cd] - root.point[cd]) < -closest_loads[0][0]:
                self._find_k_closest_loads(root.left, target_point, closest_loads, k, depth + 1)

    def _insertKDNode(self, root, point, load_id, load_type, time=None, mileage=None, price=None, dest_point=None, depth=0):
        if root is None:
            return self.KDNode(point, load_id, load_type, time, mileage, price, dest_point)

        cd = depth % 2
        if point[cd] < root.point[cd]:
            root.left = self._insertKDNode(root.left, point, load_id, load_type, time, mileage, price, dest_point, depth + 1)
        else:
            root.right = self._insertKDNode(root.right, point, load_id, load_type, time, mileage, price, dest_point, depth + 1)

        return root

    def _distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
