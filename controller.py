from calculator import InputValidator, TriangleCalculator


class Controller:

    def __init__(self, user_interface, database, notifier):
        self._ui = user_interface
        self._db = database
        self._notifier = notifier

    def run(self):
        raw = self._ui.get_sides()
        numbers = InputValidator(*raw).to_floats()

        if numbers is None:
            kind = ""
            coords = [(-2, -2), (-2, -2), (-2, -2)]
            result = {
                "kind": kind,
                "coords": coords,
                "from_db": False,
                "message": "невалидные входные данные",
            }
            self._notifier.send(f"{kind} | {coords}")
            return result

        side1, side2, side3 = numbers
        cached = self._db.get(side1, side2, side3)

        if cached is not None:
            kind, message = cached
            coords = TriangleCalculator(numbers).evaluate()[1]
            from_db = True
        else:
            kind, coords = TriangleCalculator(numbers).evaluate()
            message = "" if kind != "не треугольник" else "не треугольник"
            self._db.add(side1, side2, side3, kind, message)
            from_db = False

        self._notifier.send(f"{kind} | {coords}")

        return {
            "kind": kind,
            "coords": coords,
            "from_db": from_db,
            "message": message,
        }


def main():
    from database import TriangleDatabase
    from user_interface import ConsoleUserInterface
    from notifier import EmailNotifier

    controller = Controller(
        user_interface=ConsoleUserInterface(),
        database=TriangleDatabase("triangles.db"),
        notifier=EmailNotifier(),
    )
    result = controller.run()
    print(f"Тип треугольника: {result['kind']!r}")
    print(f"Координаты вершин: {result['coords']}")
    return 0


if __name__ == "__main__":
    main()