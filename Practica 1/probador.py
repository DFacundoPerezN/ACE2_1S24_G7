
import sqlite3
from datetime import datetime
import os
DATABASE = 'estacionamiento.db'

def registrar_entrada(tipo, rol, direccion):
    fecha_hora_actual = datetime.now()
    fecha_actual = fecha_hora_actual.strftime('%Y-%m-%d')
    hora_actual = fecha_hora_actual.strftime('%H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estacionamiento (fecha, hora, tipo, rol, direccion) VALUES (?, ?, ?, ?, ?)', (fecha_actual, hora_actual, tipo, rol, direccion))
    conn.commit()
    conn.close()

def registrar_quemado(tipo, rol, direccion):
    fecha_hora_actual = datetime.now()
    #fecha_actual = '2024-02-26'
    #hora_actual = '10:20:35'
    fecha_actual = fecha_hora_actual.strftime('%Y-%m-%d')
    hora_actual = fecha_hora_actual.strftime('%H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estacionamiento (fecha, hora, tipo, rol, direccion) VALUES (?, ?, ?, ?, ?)', (fecha_actual, hora_actual, tipo, rol, direccion))
    conn.commit()
    conn.close()

# registrar_entrada('Entrada', 'Cliente', 'Calle 1')
# registrar_entrada('mediano', 'catedratico', 'ingreso')
# registrar_entrada('mediano', 'estudiante', 'ingreso')
registrar_quemado('pequeño', 'estudiante', 'ingreso')
# registrar_entrada('pequeño', 'ajeno', 'egreso')
# registrar_entrada('mediano', 'catedratico', 'egreso')
