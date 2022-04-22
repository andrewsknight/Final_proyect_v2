import sqlite3
from balance.data_code import get_db


def insert_movement(fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad):
    db = get_db()
    print([fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad])
    cursor = db.cursor()
    statement = "INSERT INTO movimientos(fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(statement, [fecha, hora, from_moneda,
                   from_cantidad, to_moneda, to_cantidad])
    db.commit()
    return cursor.lastrowid


def update_movement(fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE movimientos SET fecha = ?, hora = ?, from_moneda = ?, from_cantidad = ?, to_moneda = ?, to_cantidad = ?, id = ?"
    cursor.execute(statement, [fecha, hora, from_moneda,
                   from_cantidad, to_moneda, to_cantidad, id])
    db.commit()
    return True


def delete_movement(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM movimientos WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True


def get_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad FROM movimientos WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()


def get_movements():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad FROM movimientos"
    cursor.execute(query)
    all_movements = cursor.fetchall()
    all_movements_array = []

    for movement in all_movements:
        id, fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad = movement
        all_movements_array.append({
            "id": id, "fecha": fecha, "hora": hora, "from_moneda": from_moneda, "from_cantidad": from_cantidad, "to_moneda": to_moneda, "to_cantidad": to_cantidad
        })
    return all_movements_array


def get_diferent_to_money():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT DISTINCT to_moneda FROM movimientos"
    cursor.execute(query)
    all_movements = cursor.fetchall() 
    all_movements_array = []

    for movement in all_movements:
        to_moneda= movement[0]
        all_movements_array.append(to_moneda)
    return all_movements_array

    
