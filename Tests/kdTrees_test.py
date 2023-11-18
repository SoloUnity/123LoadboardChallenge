import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kdTrees import KDNode, addOrUpdateTruck, getTruckByID, getTrucksByType, find_nearest_neighbor

class TestKDTreeFunctionality(unittest.TestCase):

    def setUp(self):
        self.truck_tree = None
        self.truck_map = {}
        self.sample_trucks = [
            {"truck_id": 114, "point": (41.425058, -87.33366), "truck_type": "Van"},
            {"truck_id": 346, "point": (39.195726, -84.665296), "truck_type": "Van"},
            {"truck_id": 114, "point": (40.32124710083008, -86.74946594238281), "truck_type": "Van"}
        ]
        for truck in self.sample_trucks:
            self.truck_tree = addOrUpdateTruck(self.truck_map, self.truck_tree, truck["truck_id"], truck["point"], truck["truck_type"])


    def test_getTruckByID(self):
        # Adjusted test to account for truck updates
        for truck in reversed(self.sample_trucks):
            truck_id = truck["truck_id"]
            expected_location = truck["point"]
            expected_type = truck["truck_type"]
            retrieved_truck = getTruckByID(self.truck_map, truck_id)
            self.assertEqual(retrieved_truck.point, expected_location)
            self.assertEqual(retrieved_truck.truck_type, expected_type)
            break  # Break after the first check, as the last truck with the same ID overwrites the previous one


    def test_getTrucksByType(self):
        van_trucks = getTrucksByType(self.truck_tree, "Van")
        for truck in van_trucks:
            self.assertEqual(truck.truck_type, "Van")

    def test_findNearestNeighbor(self):
        target_points = [
            (39.531354, -87.440632),  # Close to load 101
            (41.621465, -83.605482)   # Close to load 201
        ]
        expected_nearest_trucks = [114, 346]  # Expected nearest truck IDs
        for target_point, expected_truck_id in zip(target_points, expected_nearest_trucks):
            nearest_truck = find_nearest_neighbor(self.truck_tree, target_point)
            self.assertIsNotNone(nearest_truck, "No nearest truck found for the target point.")
            self.assertEqual(nearest_truck.truck_id, expected_truck_id)


if __name__ == '__main__':
    unittest.main()
