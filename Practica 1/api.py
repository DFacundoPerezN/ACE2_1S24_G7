from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from flask_sse import sse
import sqlite3
from datetime import datetime
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.dates as mdates
from datetime import datetime, timedelta


app = Flask(__name__)
socketio = SocketIO(app)

def enviar_actualizacion():
    # Esta función enviará eventos de actualización a través de SocketIO
    socketio.emit('actualizacion', {'message': 'Actualización en tiempo real'})

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


###############
DATABASE = 'estacionamiento.db'

def obtener_datos_por_rol_rango_fechas(fecha_inicio, fecha_fin):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT rol, COUNT(*) FROM estacionamiento 
        WHERE fecha BETWEEN ? AND ? 
        GROUP BY rol
    ''', (fecha_inicio, fecha_fin))
    datos = cursor.fetchall()
    conn.close()
    return datos

def crear_grafica_barras(datos):
    if not datos:
        return None

    roles = [dato[0] for dato in datos]
    cantidades = [dato[1] for dato in datos]

    fig, ax = plt.subplots()
    ax.bar(roles, cantidades, color='skyblue')
    ax.set_xlabel('Rol')
    ax.set_ylabel('Cantidad de Registros')
    ax.set_title('Cantidad de Registros por Rol')

    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Convertir la imagen en base64
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    plt.close()  # Cerrar la figura para liberar recursos

    return img_base64

@app.route('/')
# def index():
#     crear_tabla()
#     enviar_actualizacion()
#     conn = sqlite3.connect(DATABASE)
#     solo_fecha_actual = datetime.now().strftime('%Y-%m-%d')
#     cursor = conn.cursor()
def index():
    crear_tabla()
    enviar_actualizacion()
    conn = sqlite3.connect(DATABASE)
    solo_fecha_actual = datetime.now().strftime('%Y-%m-%d')
    cursor = conn.cursor()

    
    # Verificar si hay datos para la fecha actual
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE fecha="{solo_fecha_actual}"')
    cantidad_registros = cursor.fetchone()[0]

    if cantidad_registros == 0:
        # No hay datos para la fecha actual, puedes manejar esto según tus necesidades
        conn.close()
        return render_template('index.html', sin_datos=True)

    cursor.execute(f'SELECT * FROM estacionamiento WHERE fecha="{solo_fecha_actual}"')
    print("aca gat",cursor.fetchall())
    registros = cursor.fetchall()
    cursor.execute(f'SELECT * FROM estacionamiento WHERE direccion = "ingreso" and fecha="{solo_fecha_actual}"')
    ingresos = cursor.fetchall()

    cursor.execute(f'SELECT * FROM estacionamiento WHERE direccion = "egreso" and fecha="{solo_fecha_actual}"')
    egresos = cursor.fetchall()

    ###grafica vehiculo
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE tipo="mediano" and fecha="{solo_fecha_actual}"')
    mediano = cursor.fetchone()[0]
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE tipo="grande" and fecha="{solo_fecha_actual}"')
    grande = cursor.fetchone()[0]

    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE tipo="pequeño" and fecha="{solo_fecha_actual}"')
    pequeño = cursor.fetchone()[0]

    mediano = mediano * 2
    grande = grande * 4
    # cursor.execute(f'SELECT tipo, COUNT(*) FROM estacionamiento WHERE fecha="{solo_fecha_actual}" GROUP BY tipo')
    # datos_pie = cursor.fetchall()
    # Crear gráfico pie
    colores = plt.cm.Dark2.colors  # Paleta de colores 
    labels = [f'Personal\n{pequeño}',f'Mediano\n{mediano}',f'Grande\n{grande}']
    sizes = [pequeño, mediano, grande]
    fig, ax = plt.subplots()
    ax.pie(sizes, startangle=90, wedgeprops=dict(width=0.4), colors=colores)
    ax.axis('equal') 

    ax.set_title('Personas por Vehiculo ', pad=25, fontweight='bold',fontsize=22)  # Añadir título
    total_datos = sum(sizes)
    ax.text(0, 0, total_datos, ha='center', va='center', fontsize=14, color='black')
    ax.legend(labels, loc="upper left", bbox_to_anchor=(0.8, 0, 0.2, 1))  # Añadir leyenda
    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    # Convertir la imagen en base64 
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    ###grafica vehiculo
    plt.close()  # Cerrar la figura para liberar recursos

#################################################
    cursor.execute(f'SELECT rol, COUNT(*) FROM estacionamiento WHERE fecha="{solo_fecha_actual}" GROUP BY rol')
    datos_pie1 = cursor.fetchall()
    # Crear gráfico pie
    colores = plt.cm.Set1.colors  # Paleta de colores "viridis"
    labels = [f'{dato[0]}\n {dato[1]}' for dato in datos_pie1]
    sizes = [dato[1] for dato in datos_pie1]
    fig, ax = plt.subplots()
    ax.pie(sizes, startangle=90, wedgeprops=dict(width=0.4), colors=colores)
    ax.axis('equal')  
    ax.set_title('Vehiculos por Rol ', pad=25, fontweight='bold',fontsize=22)  # Añadir título
    total_datos = sum(sizes)
    ax.text(0, 0, total_datos, ha='center', va='center', fontsize=14, color='black')
    ax.legend(labels, loc="upper left", bbox_to_anchor=(0.8, 0, 0.2, 1))  # Añadir leyenda

    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    # Convertir la imagen en base64 
    img_base64_2 = base64.b64encode(img_buf.read()).decode('utf-8')
###grafica vehiculo
    plt.close()  # Cerrar la figura para liberar recursos
############
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE direccion="ingreso" and fecha="{solo_fecha_actual}"')
    ocupados = cursor.fetchone()[0]
    total_desocupados = 200 - ocupados
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE direccion="egreso" and fecha="{solo_fecha_actual}"')
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
    ax.pie(sizes,  startangle=90, wedgeprops=dict(width=0.4), colors=colores)
    ax.axis('equal') 

    ax.set_title('Espacios Ocupados', pad=25, fontweight='bold', fontsize=22)  # Añadir título
    ax.legend(labels, loc="upper left", bbox_to_anchor=(0.8, 0, 0.2, 1))  # Añadir leyenda
    total_text = ocupados
    ax.text(0, 0, total_text, ha='center', va='center', fontsize=14, color='black')
    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Convertir la imagen en base64
    img_total = base64.b64encode(img_buf.read()).decode('utf-8')

    plt.close()  # Cerrar la figura para liberar recursos

######################################################################################################################
    # datos_dashboard = obtener_datos_dashboard()
    # img_flujo = generar_grafico_flujo(datos_dashboard)
    ##########
    fecha_inicio = '2024-02-15	'  # Definir tu fecha de inicio
    fecha_fin = '2024-02-17	'  # Definir tu fecha de fin

    datos_por_rol = obtener_datos_por_rol_rango_fechas(fecha_inicio, fecha_fin)

    if datos_por_rol:
        img_flujo = crear_grafica_barras(datos_por_rol)
    ###########

    return render_template('index.html',img_flujo=img_flujo,img_total=img_total,img_base64=img_base64, img_base64_2=img_base64_2,registros=registros , ingresos=ingresos, egresos=egresos)



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


def registrar_entrada(tipo, rol, direccion):
    fecha_hora_actual = datetime.now()
    fecha_actual = fecha_hora_actual.strftime('%Y-%m-%d')
    hora_actual = fecha_hora_actual.strftime('%H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estacionamiento (fecha, hora, tipo, rol, direccion) VALUES (?, ?, ?, ?, ?)', (fecha_actual, hora_actual, tipo, rol, direccion))
    conn.commit()
    conn.close()
    enviar_actualizacion()


# registrar_entrada('grande', 'catedratico', 'ingreso')
# registrar_entrada('pequeño', 'estudiante', 'ingreso')
# registrar_entrada('mediano', 'ajeno', 'ingreso')


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
    socketio.run(app, debug=True)
