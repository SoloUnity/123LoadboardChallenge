class KDTree:
    class KDNode:
        def __init__(self, coords, load_id, load_type, load_details, left=None, right=None):
            self.coords = coords  # (latitude, longitude)
            self.load_id = load_id
            self.load_type = load_type
            self.load_details = load_details
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.load_map = {}

    def insert_load(self, origin_latitude, origin_longitude, load_id, load_type, load_details):
        coords = (origin_latitude, origin_longitude)
        if load_id in self.load_map:
            load_node = self.load_map[load_id]
            load_node.coords = coords
            load_node.load_type = load_type
            load_node.load_details = load_details
        else:
            self.root = self._insertKDNode(self.root, coords, load_id, load_type, load_details)

    def get_load_by_id(self, load_id):
        return self.load_map.get(load_id)

    def find_k_closest_loads(self, target_coords, k=5):
        closest_loads = []
        self._find_k_closest_loads(self.root, target_coords, closest_loads, k)
        
        loads = {}  # Dictionary to store load details with load ID as keys

        for node in closest_loads:
            load_id = node[1].load_id
            load = {
                "load_type": node[1].load_type,
                "coords": node[1].coords,
                "load_details": node[1].load_details,
                "distance": node[0]
            }
            loads[load_id] = load
        return loads

    def _find_k_closest_loads(self, root, target_coords, closest_loads, k, depth=0):
        if root is None:
            return

        distance = self._distance(target_coords, root.coords)

        if len(closest_loads) < k:
            closest_loads.append((distance, root))
        elif distance < closest_loads[k - 1][0]:
            closest_loads[k - 1] = (distance, root)
        
        closest_loads.sort()  

        x_or_y = depth % 2

        if target_coords[x_or_y] < root.coords[x_or_y]:
            self._find_k_closest_loads(root.left, target_coords, closest_loads, k, depth + 1)
            if abs(target_coords[x_or_y] - root.coords[x_or_y]) < closest_loads[k - 1][0]:
                self._find_k_closest_loads(root.right, target_coords, closest_loads, k, depth + 1)
        else:
            self._find_k_closest_loads(root.right, target_coords, closest_loads, k, depth + 1)
            if abs(target_coords[x_or_y] - root.coords[x_or_y]) < closest_loads[k - 1][0]:
                self._find_k_closest_loads(root.left, target_coords, closest_loads, k, depth + 1)

    def _insertKDNode(self, root, coords, load_id, load_type, load_details, depth=0):
        if root is None:
            self.load_map[load_id] = self.KDNode(coords, load_id, load_type, load_details)
            return self.load_map[load_id]
        
        x_or_y = depth % 2
        if coords[x_or_y] < root.coords[x_or_y]:
            root.left = self._insertKDNode(root.left, coords, load_id, load_type, load_details, depth + 1)
        else:
            root.right = self._insertKDNode(root.right, coords, load_id, load_type, load_details, depth + 1)

        return root

    def _distance(self, x1, x2):
        return ((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) ** 0.5
