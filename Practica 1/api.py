from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'estacionamiento.db'
hora_actual = datetime.now().time()
hora_actual = str(hora_actual)

fecha_actual = datetime.now().strftime('%Y-%m-%d')
fecha_actual = str(fecha_actual)

def crear_tabla():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estacionamiento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        tipo TEXT NOT NULL,
        rol TEXT NOT NULL,
        direccion TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    crear_tabla()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estacionamiento')
    registros = cursor.fetchall()
    cursor.execute('SELECT * FROM estacionamiento WHERE direccion = "ingreso"')
    ingresos = cursor.fetchall()
    cursor.execute('SELECT * FROM estacionamiento WHERE direccion = "egreso"')
    egresos = cursor.fetchall()

    ###grafica vehiculo
    cursor.execute('SELECT tipo, COUNT(*) FROM estacionamiento GROUP BY tipo')
    datos_pie = cursor.fetchall()


    # Crear gráfico pie
    labels = [f'{dato[0]}\n {dato[1]}' for dato in datos_pie]
    sizes = [dato[1] for dato in datos_pie]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
    ax.axis('equal') 

    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Convertir la imagen en base64 
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    ###grafica vehiculo

    plt.close()  # Cerrar la figura para liberar recursos


    cursor.execute('SELECT rol, COUNT(*) FROM estacionamiento GROUP BY rol')
    datos_pie1 = cursor.fetchall()


    # Crear gráfico pie
    labels = [f'{dato[0]}\n {dato[1]}' for dato in datos_pie1]
    sizes = [dato[1] for dato in datos_pie1]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
    ax.axis('equal')  

    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Convertir la imagen en base64 
    img_base64_2 = base64.b64encode(img_buf.read()).decode('utf-8')
    ###grafica vehiculo

    plt.close()  # Cerrar la figura para liberar recursos

############
    cursor.execute('SELECT COUNT(*) FROM estacionamiento WHERE direccion="ingreso"')
    ocupados = cursor.fetchone()[0]
    total_desocupados = 200 - ocupados
    cursor.execute('SELECT COUNT(*) FROM estacionamiento WHERE direccion="egreso"')
    ocupados_egreso = cursor.fetchone()[0]
    if total_desocupados < 200:
        total_desocupados = total_desocupados + ocupados_egreso
        ocupados= ocupados - ocupados_egreso
    conn.close()

    # Crear gráfico de anillo para mostrar ocupados, desocupados y el total
    total = 200
    labels = [f'Ocupados\n{ocupados}', f'Desocupados\n{total_desocupados}']
    sizes = [ocupados, total_desocupados]
    colores = ['#0C22FF', '#D3D6F4']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4), colors=colores)
    ax.axis('equal') 

    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Convertir la imagen en base64
    img_total = base64.b64encode(img_buf.read()).decode('utf-8')

    plt.close()  # Cerrar la figura para liberar recursos

    return render_template('index.html', img_total=img_total,img_base64=img_base64, img_base64_2=img_base64_2,registros=registros , ingresos=ingresos, egresos=egresos)


def registro_directo(placa, hora_entrada, direccion):
    crear_tabla()
    
    # Conectar a la base de datos y agregar un nuevo registro
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estacionamiento (fecha, hora, tipo, rol, direccion)) VALUES (?, ?, ?, "ingreso")', (placa, hora_entrada, direccion))
    conn.commit()
    conn.close()

@app.route('/registrar')
def registrar_desde_python():

    tipo = 'grande'
    rol = 'catedratico'
    direccion = 'ingreso'

    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estacionamiento (fecha, hora, tipo, rol, direccion) VALUES (?, ?, ?, ?, ?)', (fecha_actual,hora_actual, tipo, rol, direccion))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Nueva ruta para limpiar la base de datos
@app.route('/limpiar_base_de_datos')
def limpiar_base_de_datos():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estacionamiento')
    conn.commit()
    conn.close()

    return redirect(url_for('index'))



@app.route('/eliminar_base_de_datos')
def eliminar_base_de_datos():
    try:
        os.remove(DATABASE)
        return "Base de datos eliminada exitosamente."
    except FileNotFoundError:
        return "La base de datos no existe."
    

if __name__ == '__main__':
    app.run(debug=True)