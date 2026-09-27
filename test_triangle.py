import unittest
import sys
from io import StringIO
from unittest.mock import patch
import math

from main import InputValidator, TriangleCalculator, Main


class TestInputValidator(unittest.TestCase):
    def test_valid_integers(self):
        validator = InputValidator("3", "4", "5")
        result = validator.to_floats()
        self.assertEqual(result, [3.0, 4.0, 5.0])


    def test_valid_floats(self):
        validator = InputValidator("3.5", "4.5", "5.5")
        result = validator.to_floats()
        self.assertEqual(result, [3.5, 4.5, 5.5])


 
    def test_invalid_letters(self):
        validator = InputValidator("abc", "4", "5")
        self.assertIsNone(validator.to_floats())



    def test_invalid_empty_string(self):
        validator = InputValidator("", "4", "5")
        self.assertIsNone(validator.to_floats())



    def test_invalid_none(self):
        validator = InputValidator(None, "4", "5")
        self.assertIsNone(validator.to_floats())



    def test_invalid_infinity(self):
        validator = InputValidator("inf", "4", "5")
        self.assertIsNone(validator.to_floats())



    def test_invalid_nan(self):
        validator = InputValidator("nan", "4", "5")
        self.assertIsNone(validator.to_floats())



class TestTriangleCalculator(unittest.TestCase):

    def test_equilateral_triangle(self):
        calc = TriangleCalculator([3.0, 3.0, 3.0])
        kind, coords = calc.evaluate()
        self.assertEqual(kind, "равносторонний")
        self.assertEqual(len(coords), 3)



    def test_isosceles_triangle(self):
        calc = TriangleCalculator([5.0, 5.0, 6.0])
        kind, coords = calc.evaluate()
        self.assertEqual(kind, "равнобедренный")
        self.assertEqual(len(coords), 3)



    def test_scalene_triangle(self):
        calc = TriangleCalculator([3.0, 4.0, 5.0])
        kind, coords = calc.evaluate()
        self.assertEqual(kind, "разносторонний")
        self.assertEqual(len(coords), 3)



    def test_not_triangle_negative_side(self):
        calc = TriangleCalculator([-3.0, 4.0, 5.0])
        kind, coords = calc.evaluate()
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])



    def test_not_triangle_zero_side(self):
        calc = TriangleCalculator([0.0, 4.0, 5.0])
        kind, coords = calc.evaluate()
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])



    def test_not_triangle_violates_inequality(self):
        calc = TriangleCalculator([1.0, 2.0, 10.0])
        kind, coords = calc.evaluate()
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])



    def test_degenerate_triangle(self):
        calc = TriangleCalculator([1.0, 2.0, 3.0])
        kind, coords = calc.evaluate()
        self.assertEqual(kind, "не треугольник")



    def test_vertices_coordinates_in_range(self):
        calc = TriangleCalculator([3.0, 4.0, 5.0])
        kind, coords = calc.evaluate()
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)



    def test_vertices_are_integers(self):
        calc = TriangleCalculator([3.0, 4.0, 5.0])
        kind, coords = calc.evaluate()
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)



class TestMainFunction(unittest.TestCase):

    @patch('sys.argv', ['program.py', '3', '4', '5'])
    def test_main_with_argv_scalene(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Main()
            output = fake_out.getvalue()
            self.assertIn("разносторонний", output)
            self.assertIn("Координаты вершин", output)



    @patch('sys.argv', ['program.py', '3', '3', '3'])
    def test_main_with_argv_equilateral(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Main()
            output = fake_out.getvalue()
            self.assertIn("равносторонний", output)



    @patch('sys.argv', ['program.py', 'abc', '4', '5'])
    def test_main_with_invalid_argv(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Main()
            output = fake_out.getvalue()
            self.assertIn("Тип треугольника: ''", output)
            self.assertIn("[(-2, -2), (-2, -2), (-2, -2)]", output)



    @patch('sys.argv', ['program.py'])
    @patch('builtins.input', side_effect=['3', '4', '5'])
    def test_main_with_user_input(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Main()
            output = fake_out.getvalue()
            self.assertIn("разносторонний", output)


if __name__ == '__main__':
    unittest.main(verbosity=2)