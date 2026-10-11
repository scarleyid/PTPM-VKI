import unittest
from unittest.mock import MagicMock, patch

from calculator import InputValidator, TriangleCalculator
from database import TriangleDatabase
from controller import Controller
from user_interface import UserInterface, ConsoleUserInterface
from notifier import Notifier, EmailNotifier



class TestTriangleDatabase(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db._conn.close()
        self.db = None

    def test_add_get_delete_roundtrip(self):
        self.db.add(3.0, 4.0, 5.0, "разносторонний", "")
        self.assertEqual(self.db.get(3.0, 4.0, 5.0), ("разносторонний", ""))
        self.assertTrue(self.db.delete(3.0, 4.0, 5.0))
        self.assertIsNone(self.db.get(3.0, 4.0, 5.0))

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.db.get(1.0, 2.0, 3.0))



class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.notifier = MagicMock(spec=Notifier)
        self.ui = MagicMock(spec=UserInterface)
        self.ui.get_sides.return_value = ("3", "4", "5")
        self.controller = Controller(self.ui, self.db, self.notifier)

    def tearDown(self):
        self.controller = None
        self.ui.reset_mock()
        self.ui = None
        self.notifier.reset_mock()
        self.notifier = None
        self.db._conn.close()
        self.db = None

    def test_full_scenario_new_data_calculates_and_saves(self):
        result = self.controller.run()

        self.assertEqual(result["kind"], "разносторонний")
        self.assertFalse(result["from_db"])
        self.assertIsNotNone(self.db.get(3.0, 4.0, 5.0))
        self.notifier.send.assert_called_once()
        sent = self.notifier.send.call_args[0][0]
        self.assertIn("разносторонний", sent)

    def test_full_scenario_cached_data_taken_from_db(self):
        self.ui.get_sides.return_value = ("5", "5", "6")
        self.db.add(5.0, 5.0, 6.0, "равнобедренный", "")

        result = self.controller.run()

        self.assertEqual(result["kind"], "равнобедренный")
        self.assertTrue(result["from_db"])
        self.notifier.send.assert_called_once()

    def test_integration_non_numeric_input_uses_mock_ui(self):
        self.ui.get_sides.return_value = ("abc", "4", "5")

        result = self.controller.run()

        self.assertEqual(result["kind"], "")
        self.assertEqual(result["coords"], [(-2, -2), (-2, -2), (-2, -2)])
        self.assertIsNone(self.db.get(0.0, 4.0, 5.0))
        self.notifier.send.assert_called_once()
class TestControllerIntegrationWithRealConsoleUI(unittest.TestCase):
 
    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.notifier = MagicMock(spec=Notifier)
        self.controller = Controller(
            ConsoleUserInterface(), self.db, self.notifier
        )
        self._input_patcher = patch("builtins.input", side_effect=["10", "1", "1"])
        self._mock_input = self._input_patcher.start()

    def tearDown(self):
        self._input_patcher.stop()
        self.notifier.reset_mock()
        self.notifier = None
        self.db._conn.close()
        self.db = None
        self.controller = None

    def test_integration_invalid_triangle_with_real_console_ui(self):
        result = self.controller.run()

        self.assertEqual(result["kind"], "не треугольник")
        self.assertIsNotNone(self.db.get(10.0, 1.0, 1.0))
        self.notifier.send.assert_called_once()
        self.assertEqual(self._mock_input.call_count, 3)