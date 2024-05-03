import mysql.connector
from mysql.connector import Error
from datetime import datetime

conexion = None
cursor = None

try:
    # Establecer la conexión con la base de datos
    conexion = mysql.connector.connect(
        host='basepy2.cve48c8m8loo.us-east-2.rds.amazonaws.com',
        user='root',
        password='secret1234',
        database='registros_db'
    )

    # Crear un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # Comprobar la conexión
    cursor.execute("SELECT VERSION()")
    resultado = cursor.fetchone()
    print("Conexión exitosa a MySQL. Versión del servidor:", resultado[0])

    # Obtener la fecha y hora actuales
    now = datetime.now()
    fecha_formateada = now.strftime("%Y-%m-%d")
    hora_formateada = now.strftime("%H:%M:%S")

    # Insertar un registro en la base de datos
    consulta = "INSERT INTO registros (logueado, fecha, hora) VALUES (%s, %s, %s)"
    cursor.execute(consulta, ("si", fecha_formateada, hora_formateada))
    conexion.commit()

except Error as err:
    print(f"Error al conectar a la base de datos: {err}")

finally:
    if cursor:
        cursor.close()
    if conexion:
        conexion.close()


def mandar(logout):
    conexion = None
    cursor = None

    try:
        # Establecer la conexión con la base de datos
        conexion = mysql.connector.connect(
            host='basepy2.cve48c8m8loo.us-east-2.rds.amazonaws.com',
            user='root',
            password='secret1234',
            database='registros_db'
        )

        # Crear un cursor para ejecutar comandos SQL
        cursor = conexion.cursor()

        # Comprobar la conexión
        cursor.execute("SELECT VERSION()")
        resultado = cursor.fetchone()
        print("Conexión exitosa a MySQL. Versión del servidor:", resultado[0])

        # Obtener la fecha y hora actuales
        now = datetime.now()
        fecha_formateada = now.strftime("%Y-%m-%d")
        hora_formateada = now.strftime("%H:%M:%S")
        hora_formateada=logout
        # Insertar un registro en la base de datos
        consulta = "INSERT INTO registros (logueado, fecha, hora) VALUES (%s, %s, %s)"
        cursor.execute(consulta, ("si", fecha_formateada, hora_formateada))
        conexion.commit()

    except Error as err:
        print(f"Error al conectar a la base de datos: {err}")

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
