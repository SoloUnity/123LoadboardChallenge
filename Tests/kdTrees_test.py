import unittest
from loader import KDTreeLoads
class TestKDTree(unittest.TestCase):
    def setUp(self):
        self.kdTree = KDTreeLoads.KDTree()

    def test_insert_load_with_details(self):
        # Test if load with additional details is inserted correctly
        load_id = 1
        origin_latitude = 40.0
        origin_longitude = -75.0
        load_type = "TypeA"
        load_details = {
            "time": "2023-11-17T11:31:35.0481646-05:00",
            "mileage": 2166.0,
            "price": 3150.0
        }

        self.kdTree.insert_load(origin_latitude, origin_longitude, load_id, load_type, load_details)

        # Check if the load is present in the KDTree
        load_node = self.kdTree.get_load_by_id(load_id)
        self.assertIsNotNone(load_node)
        self.assertEqual(load_node.load_id, load_id)
        self.assertEqual(load_node.coords, (origin_latitude, origin_longitude))
        self.assertEqual(load_node.load_type, load_type)
        self.assertEqual(load_node.load_details, load_details)

    def test_find_k_closest_loads(self):
        # Test finding the closest loads
        origin_coords = (0.0, 5.0)

        # Insert some sample loads
        self.kdTree.insert_load(1.0, 4.0, 2, "TypeB", {"time": "2023-11-17T12:00:00", "mileage": 2500.0, "price": 4000.0})
        self.kdTree.insert_load(39.5, -76.0, 3, "TypeA", {"time": "2023-11-17T12:30:00", "mileage": 1800.0, "price": 3000.0})
        self.kdTree.insert_load(40.2, -74.5, 4, "TypeC", {"time": "2023-11-17T13:00:00", "mileage": 3000.0, "price": 5000.0})
        self.kdTree.insert_load(38.8, -75.5, 5, "TypeA", {"time": "2023-11-17T13:30:00", "mileage": 2200.0, "price": 3500.0})
        self.kdTree.insert_load(20.9, 15.2, 6, "TypeB", {"time": "2023-11-17T14:00:00", "mileage": 2800.0, "price": 4500.0})

        # Find the closest 3 loads
        closest_loads = self.kdTree.find_k_closest_loads(origin_coords, k=2)
        print(closest_loads)
        # Validate the result
        self.assertEqual(len(closest_loads), 2)
        
        # Add more specific assertions based on your expected results

if __name__ == '__main__':
    unittest.main()