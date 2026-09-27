import unittest
from Delivery import calculate_delivery_cost


class TestCalculateDeliveryCost(unittest.TestCase):

    def test_valid_normal_package(self):
        cost, date = calculate_delivery_cost(3.0, 500, "обычный")
        self.assertEqual(cost, 2700)
        self.assertEqual(date, "2026-09-04")

    def test_valid_fragile_package(self):
        cost, date = calculate_delivery_cost(3.0, 500, "хрупкий")
        self.assertEqual(cost, 3000)
        self.assertEqual(date, "2026-09-04")

    def test_valid_dangerous_package(self):
        cost, date = calculate_delivery_cost(3.0, 500, "опасный")
        self.assertEqual(cost, 3700)
        self.assertEqual(date, "2026-09-04")

    def test_weight_over_5kg_multiplier(self):
        cost, date = calculate_delivery_cost(10.0, 500, "обычный")
        self.assertEqual(cost, 3240)
        self.assertEqual(date, "2026-09-04")

    def test_weight_over_20kg_multiplier(self):
        cost, date = calculate_delivery_cost(25.0, 500, "обычный")
        self.assertEqual(cost, 4050)
        self.assertEqual(date, "2026-09-04")

    def test_express_delivery(self):
        cost, date = calculate_delivery_cost(3.0, 500, "обычный", True)
        self.assertEqual(cost, 1350)
        self.assertEqual(date, "2026-09-04")

    def test_long_distance(self):
        cost, date = calculate_delivery_cost(3.0, 5000, "обычный")
        self.assertEqual(cost, 25200)
        self.assertEqual(date, "2026-09-13")

    def test_weight_too_low(self):
        cost, date = calculate_delivery_cost(0.05, 500, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_too_high(self):
        cost, date = calculate_delivery_cost(51.0, 500, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_package_type(self):
        cost, date = calculate_delivery_cost(3.0, 500, "неизвестный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")


if __name__ == "__main__":
    unittest.main(verbosity=2)