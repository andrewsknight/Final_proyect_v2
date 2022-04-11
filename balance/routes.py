from balance import app
import sqlite3

@app("/api/v1/movimientos")
def lista_movimientos():
    con = sqlite3.connect(self.origen_datos)
    cur = con.cursor()

    cur.execute(consulta, params)

    resultado = self.results(cur, con)

    con.close()
    ("""
                        SELECT fecha, hora, concepto, es_ingreso, cantidad, id
                          FROM movimientos
                         WHERE id = ?      
                    """, (id,))

@app("/api/v1/movimiento/id")
def movimiento():
    pass