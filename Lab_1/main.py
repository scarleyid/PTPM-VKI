import math
import sys
import logging

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)


class InputValidator:
    def __init__(self, side1, side2, side3):
        self._values = (side1, side2, side3)

    def to_floats(self):
        logger.debug("Валидация входных данных: %s", self._values)
        if not self._is_valid():
            logger.warning(
                "Неуспешный запрос: параметры=%s, ошибка=невалидные значения "
                "(не число, inf или nan)", self._values
            )
            return None
        result = [float(value) for value in self._values]
        logger.debug("Успешная валидация: стороны=%s", result)
        return result

    def _is_valid(self):
        for value in self._values:
            try:
                number = float(value)
            except (TypeError, ValueError) as exc:
                logger.debug(
                    "Значение %r не преобразуется во float: %s", value, exc,
                    exc_info=True
                )
                return False
            if not math.isfinite(number):
                logger.debug("Значение %r не конечно (inf/nan)", value)
                return False
        return True


class TriangleCalculator:
    def __init__(self, sides):
        self._a, self._b, self._c = sides
        logger.debug("TriangleCalculator создан со сторонами: %s", sides)

    def evaluate(self):
        a, b, c = self._a, self._b, self._c
        logger.info(
            "Запрос на обработку треугольника: a=%s, b=%s, c=%s", a, b, c
        )

        if a <= 0 or b <= 0 or c <= 0:
            logger.warning(
                "Неуспешный запрос: параметры=(%s, %s, %s), "
                "ошибка=неположительная сторона", a, b, c
            )
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        if a + b <= c or a + c <= b or b + c <= a:
            logger.warning(
                "Неуспешный запрос: параметры=(%s, %s, %s), "
                "ошибка=нарушено неравенство треугольника", a, b, c
            )
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        if a == b == c:
            kind = "равносторонний"
        elif a == b or b == c or a == c:
            kind = "равнобедренный"
        else:
            kind = "разносторонний"

        coords = self._calculate_vertices()
        logger.info(
            "Успешный запрос: параметры=(%s, %s, %s), тип=%s, вершины=%s",
            a, b, c, kind, coords
        )
        return kind, coords

    def _calculate_vertices(self):
        try:
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
            logger.debug("Вычисленные координаты вершин: %s", coords)
            return coords
        except Exception as exc:
            logger.error(
                "Неуспешный запрос: параметры=(%s, %s, %s), "
                "ошибка при вычислении вершин: %s",
                self._a, self._b, self._c, exc,
                exc_info=True
            )
            raise


def Main():
    logger.info("Приложение запущено")

    if len(sys.argv) == 4:
        side1, side2, side3 = sys.argv[1], sys.argv[2], sys.argv[3]
        logger.info("Источник данных: аргументы командной строки")
    else:
        side1 = input("Введите длину стороны A: ")
        side2 = input("Введите длину стороны B: ")
        side3 = input("Введите длину стороны C: ")
        logger.info("Источник данных: ввод пользователя")

    logger.info(
        "Параметры запроса: side1=%r, side2=%r, side3=%r",
        side1, side2, side3
    )

    numbers = InputValidator(side1, side2, side3).to_floats()
    if numbers is None:
        logger.error(
            "Неуспешный запрос: параметры=(%r, %r, %r), "
            "ошибка=невалидные входные данные",
            side1, side2, side3
        )
        print("Тип треугольника: ''")
        print("Координаты вершин: [(-2, -2), (-2, -2), (-2, -2)]")
        logger.info("Приложение завершено с кодом 0 (невалидный ввод)")
        return 0

    kind, coords = TriangleCalculator(numbers).evaluate()
    print(f"Тип треугольника: {kind!r}")
    print(f"Координаты вершин: {coords}")
    logger.info("Приложение завершено с кодом 0 (успех)")
    return 0


if __name__ == "__main__":
    Main()