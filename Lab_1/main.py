import math
import sys


class InputValidator:
    def __init__(self, side1, side2, side3):
        self._values = (side1, side2, side3)

    def to_floats(self):
        if not self._is_valid():
            return None
        return [float(value) for value in self._values]

    def _is_valid(self):
        for value in self._values:
            try:
                number = float(value)
            except (TypeError, ValueError):
                return False
            if not math.isfinite(number):
                return False
        return True


class TriangleCalculator:
    def __init__(self, sides):
        self._a, self._b, self._c = sides

    def evaluate(self):
        a, b, c = self._a, self._b, self._c
        if a <= 0 or b <= 0 or c <= 0:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]
        if a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]
        if a == b == c:
            kind = "равносторонний"
        elif a == b or b == c or a == c:
            kind = "равнобедренный"
        else:
            kind = "разносторонний"
        return kind, self._calculate_vertices()

    def _calculate_vertices(self):
        a, b, c = self._a, self._b, self._c
        x1, y1 = 0.0, 0.0
        x2, y2 = a, 0.0
        cos_angle = (a * a + b * b - c * c) / (2.0 * a * b)
        cos_angle = max(-1.0, min(1.0, cos_angle))
        x3 = b * cos_angle
        diff = max(0.0, b * b - x3 * x3)
        y3 = math.sqrt(diff)
        points = [(x1, y1), (x2, y2), (x3, y3)]
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        scale = min(100.0 / width, 100.0 / height) if width and height else 1.0
        coords = []
        for px, py in points:
            nx = max(0, min(100, int(round((px - min(xs)) * scale))))
            ny = max(0, min(100, int(round((py - min(ys)) * scale))))
            coords.append((nx, ny))
        return coords


def Main():
    if len(sys.argv) == 4:
        side1, side2, side3 = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        side1 = input("Введите длину стороны A: ")
        side2 = input("Введите длину стороны B: ")
        side3 = input("Введите длину стороны C: ")

    numbers = InputValidator(side1, side2, side3).to_floats()
    if numbers is None:
        print("Тип треугольника: ''")
        print("Координаты вершин: [(-2, -2), (-2, -2), (-2, -2)]")
        return 0

    kind, coords = TriangleCalculator(numbers).evaluate()
    print(f"Тип треугольника: {kind!r}")
    print(f"Координаты вершин: {coords}")
    return 0


if __name__ == "__main__":
    Main()