import sqlite3
DATABASE_NAME = "movimientos.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    table = """CREATE TABLE IF NOT EXISTS movimientos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                from_moneda TEXT NOT NULL,
                from_cantidad DOUBLE NOT NULL,
                to_moneda TEXT NOT NULL,
                to_cantidad DOUBLE NOT NULL
            )
            """

    db = get_db()
    cursor = db.cursor()

    cursor.execute(table)
