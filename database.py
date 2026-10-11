import sqlite3


class TriangleDatabase:
    

    def __init__(self, db_path=":memory:"):
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS triangles (
                side1 REAL NOT NULL,
                side2 REAL NOT NULL,
                side3 REAL NOT NULL,
                kind TEXT NOT NULL,
                message TEXT,
                PRIMARY KEY (side1, side2, side3)
            )
            """
        )
        self._conn.commit()

    def add(self, side1, side2, side3, kind, message=""):
        self._conn.execute(
            "INSERT OR REPLACE INTO triangles "
            "(side1, side2, side3, kind, message) VALUES (?, ?, ?, ?, ?)",
            (side1, side2, side3, kind, message),
        )
        self._conn.commit()

    def get(self, side1, side2, side3):
        cur = self._conn.execute(
            "SELECT kind, message FROM triangles "
            "WHERE side1=? AND side2=? AND side3=?",
            (side1, side2, side3),
        )
        return cur.fetchone()

    def delete(self, side1, side2, side3):
        cur = self._conn.execute(
            "DELETE FROM triangles "
            "WHERE side1=? AND side2=? AND side3=?",
            (side1, side2, side3),
        )
        self._conn.commit()
        return cur.rowcount > 0