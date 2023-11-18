class KDTree:
    class KDNode:
        def __init__(self, point, load_id, load_type, left=None, right=None):
            self.point = point  # (latitude, longitude)
            self.load_id = load_id
            self.load_type = load_type
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.load_map = {}

    def insert_load(self, origin_latitude, origin_longitude, load_id, load_type):
        point = (origin_latitude, origin_longitude)

        if load_id in self.load_map:
            load_node = self.load_map[load_id]
            load_node.point = point
            load_node.load_type = load_type
        else:
            self.root = self._insertKDNode(self.root, point, load_id, load_type)
            self.load_map[load_id] = self.root

    def _insertKDNode(self, root, point, load_id, load_type, depth=0):
        if root is None:
            return self.KDNode(point, load_id, load_type)

        cd = depth % 2
        if point[cd] < root.point[cd]:
            root.left = self._insertKDNode(root.left, point, load_id, load_type, depth + 1)
        else:
            root.right = self._insertKDNode(root.right, point, load_id, load_type, depth + 1)

        return root

    def get_load_by_id(self, load_id):
        return self.load_map.get(load_id)

    def find_nearest_load(self, target_point):
        return self._find_nearest_load(self.root, target_point)

    def _find_nearest_load(self, root, target_point, depth=0, best=None):
        if root is None:
            return best

        if best is None or self._distance(target_point, root.point) < self._distance(target_point, best.point):
            best = root

        cd = depth % 2

        if target_point[cd] < root.point[cd]:
            best = self._find_nearest_load(root.left, target_point, depth + 1, best)
            if abs(target_point[cd] - root.point[cd]) < self._distance(target_point, best.point):
                best = self._find_nearest_load(root.right, target_point, depth + 1, best)
        else:
            best = self._find_nearest_load(root.right, target_point, depth + 1, best)
            if abs(target_point[cd] - root.point[cd]) < self._distance(target_point, best.point):
                best = self._find_nearest_load(root.left, target_point, depth + 1, best)

        return best

    def _distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
