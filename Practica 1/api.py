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
import pandas as pd
import numpy as np
#from scipy.interpolate import interp1d
#from scipy.interpolate import UnivariateSpline

import matplotlib
matplotlib.use('Agg')  # Desactivar manejo de ventanas emergentes de GUI
import matplotlib.pyplot as plt

app = Flask(__name__)
socketio = SocketIO(app)

# def enviar_actualizacion():
#     # Esta función enviará eventos de actualización a través de SocketIO
#     socketio.emit('actualizacion', {'message': 'Actualización en tiempo real'})

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
    # enviar_actualizacion()
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
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE tipo="mediano" and direccion = "egreso" and fecha="{solo_fecha_actual}"')
    mediano1 = cursor.fetchone()[0]
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE tipo="grande" and direccion = "egreso" and fecha="{solo_fecha_actual}"')
    grande1 = cursor.fetchone()[0]
    cursor.execute(f'SELECT COUNT(*) FROM estacionamiento WHERE tipo="pequeño" and direccion = "egreso" and fecha="{solo_fecha_actual}"')
    pequeño1 = cursor.fetchone()[0]
    mediano = mediano * 2
    grande = grande * 4
    pequeño = pequeño * 1
    pequeño1 = pequeño1 * 1
    mediano1 = mediano1 * 2
    grande1 = grande1 * 4
    total_pequeño = pequeño - pequeño1
    total_mediano = mediano - mediano1
    total_grande = grande - grande1

    # cursor.execute(f'SELECT tipo, COUNT(*) FROM estacionamiento WHERE fecha="{solo_fecha_actual}" GROUP BY tipo')
    # datos_pie = cursor.fetchall()
    # Crear gráfico pie
    colores = plt.cm.Dark2.colors  # Paleta de colores 
    labels = [f'Personal\n{total_pequeño}',f'Mediano\n{total_mediano}',f'Grande\n{total_grande}']
    sizes = [total_pequeño, total_mediano, total_grande]
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
    cursor.execute(f'SELECT rol, COUNT(*) FROM estacionamiento WHERE fecha="{solo_fecha_actual}" AND direccion=="egreso" GROUP BY rol')
    datos_pie = cursor.fetchall()
    cursor.execute(f'SELECT rol, COUNT(*) FROM estacionamiento WHERE fecha="{solo_fecha_actual}" AND direccion!="egreso" GROUP BY rol')
    datos_pie1 = cursor.fetchall()
    print("=========================================")
    print("datos_pie",datos_pie )
    # datos_pie1[0][1] =  datos_pie1[0][1]- datos_pie[0][1]
    # print("total_datos",total_datos)
    # Crear gráfico pie
    # datos_pie1[1] = datos_pie1[1] + datos_pie[1]
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

    return render_template('index.html',img_total=img_total,img_base64=img_base64, img_base64_2=img_base64_2,registros=registros , ingresos=ingresos, egresos=egresos)


@app.route('/', methods=['GET', 'POST'])




@app.route('/index2.html', methods=['GET', 'POST'])
def otra_ruta():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fecha, rol, COUNT(*) as total
        FROM estacionamiento
        WHERE direccion = 'ingreso'
        GROUP BY fecha, rol
        ORDER BY fecha
    ''')
    datos_ingresos = cursor.fetchall()

    # Obtener las fechas únicas y los roles únicos
    fechas_unicas = sorted(set(fecha for fecha, _, _ in datos_ingresos))
    roles_unicos = sorted(set(rol for _, rol, _ in datos_ingresos))

    # Asignar colores a cada rol
    colores_por_rol = {rol: plt.cm.Set1.colors[i % len(plt.cm.Set1.colors)] for i, rol in enumerate(roles_unicos)}

    # Crear gráfica de barras y leyenda
    fig, ax = plt.subplots()

    # Configurar la posición de las barras para cada fecha
    width = 0.4  # Ajusta el ancho de las barras según tus preferencias
    for i, fecha in enumerate(fechas_unicas):
        total_por_rol = {rol: 0 for rol in roles_unicos}
        for _, rol, total in datos_ingresos:
            if _ == fecha:
                total_por_rol[rol] = total
        posiciones = [i + (width * j) for j, rol in enumerate(roles_unicos)]
        colores = [colores_por_rol[rol] for rol in roles_unicos]
        ax.bar(posiciones, [total_por_rol[rol] for rol in roles_unicos], width=width, label=fecha, color=colores)

    # Configurar la gráfica
    # ax.set_xlabel('Roles')
    # ax.set_ylabel('Total acumulado')
    ax.set_title(' Gráfica de historial de tipos de vehículo por rol', pad=25, fontweight='bold', fontsize=22)

    # Agregar leyenda separada
    handles = [plt.Rectangle((0,0),1,1, color=colores_por_rol[rol], ec="k") for rol in roles_unicos]
    labels = roles_unicos
    ax.legend(handles, labels, title="Roles", bbox_to_anchor=(1, 1), loc="upper left")

    # Ajustar las etiquetas del eje x para mostrar todas las fechas
    ax.set_xticks([i + (width * (len(roles_unicos) - 1) / 2) for i in range(len(fechas_unicas))])
    ax.set_xticklabels(fechas_unicas, rotation=45, ha='right')

    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)

    # Convertir la imagen en base64
    img_barras = base64.b64encode(img_buf.read()).decode('utf-8')

    # Cerrar la conexión y la figura para liberar recursos
    conn.close()
    plt.close()


    ##################grafica de ingresos
    # conn = sqlite3.connect(DATABASE)
    # cursor = conn.cursor()

    # cursor.execute('''
    #     SELECT fecha, COUNT(*) as total_ingresos
    #     FROM estacionamiento
    #     WHERE direccion = 'ingreso'
    #     GROUP BY fecha
    #     ORDER BY fecha
    # ''')
    # datos_ingresos = cursor.fetchall()

    # # Convertir fechas a tiempo en segundos desde la época
    # fechas, total_ingresos = zip(*datos_ingresos)
    # fechas_num = [datetime.strptime(fecha, '%Y-%m-%d').timestamp() for fecha in fechas]

    # # Interpolación cúbica para obtener curvas suavizadas
    # # Aumentamos el número de puntos de control
    # spline = UnivariateSpline(fechas_num, total_ingresos, k=2, s=0)

    # # Crear nuevos puntos de datos para una representación más suave
    # fechas_smooth = np.linspace(min(fechas_num), max(fechas_num), 300)
    # total_ingresos_smooth = spline(fechas_smooth)

    # fig, ax = plt.subplots()

    # # ax.fill_between(fechas_smooth, total_ingresos_smooth, color='skyblue', alpha=0.4)
    # ax.plot(fechas_smooth, total_ingresos_smooth, marker='o', markersize=2, linestyle='-', color='b', label='Ingresos')
    # ax.scatter(fechas_num, total_ingresos, color='red')

    # # Configurar la gráfica
    # ax.set_xlabel('Fecha')
    # ax.set_ylabel('Total de ingresos')
    # ax.set_title('Variación de Ingresos por Fecha')

    # # Ajustar las etiquetas del eje x para mostrar todas las fechas
    # ax.set_xticks(fechas_num)
    # ax.set_xticklabels(fechas, rotation=45, ha='right')

    # ax.legend()

    # # Guardar la figura en un objeto BytesIO
    # img_buf = BytesIO()
    # plt.savefig(img_buf, format='png', bbox_inches='tight')
    # img_buf.seek(0)

    # # Convertir la imagen en base64
    # img_ingresos = base64.b64encode(img_buf.read()).decode('utf-8')

    # # Cerrar la conexión y la figura para liberar recursos
    # conn.close()
    # plt.close()

# jiijjiij
    
    img_ingresos = None

    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        print("Datos recibidos ")
        print(fecha_inicio,"inicio")
        print(fecha_fin,"fin")

        # Llama a tu función con las fechas recibidas
    # fecha_inicio = '2024-02-27'
    # fecha_fin = '2024-02-29'

        img_ingresos = generar_grafica_ingresos_por_fecha(fecha_inicio, fecha_fin)


    return render_template('index2.html', img_barras=img_barras,img_ingresos=img_ingresos)

def generar_grafica_ingresos_por_fecha(fecha_inicio, fecha_fin):
    # Establecer conexión a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT fecha, COUNT(*) as total_ingresos
        FROM estacionamiento
        WHERE direccion = 'ingreso'
        AND fecha BETWEEN ? AND ?
        GROUP BY fecha
        ORDER BY fecha
    ''', (fecha_inicio, fecha_fin))

    datos_ingresos = cursor.fetchall()

    # Convertir fechas a tiempo en segundos desde la época
    fechas, total_ingresos = zip(*datos_ingresos)
    fechas_num = [datetime.strptime(fecha, '%Y-%m-%d').timestamp() for fecha in fechas]
    # total_ingresos = np.log(total_ingresos)

    # Interpolación cúbica para obtener curvas suavizadas
    # Aumentamos el número de puntos de control
    spline = UnivariateSpline(fechas_num, total_ingresos, k=2, s=0)

    # Crear nuevos puntos de datos para una representación más suave
    fechas_smooth = np.linspace(min(fechas_num), max(fechas_num), 300)
    total_ingresos_smooth  = spline(fechas_smooth)
    # total_ingresos_smooth = np.exp(total_ingresos_smooth_log )

    fig, ax = plt.subplots()

    # ax.fill_between(fechas_smooth, total_ingresos_smooth, color='skyblue', alpha=0.4)
    ax.plot(fechas_smooth, total_ingresos_smooth, '-o', markersize=2, color='b', label='Ingresos')
    ax.scatter(fechas_num, total_ingresos, color='red')

    # Configurar la gráfica
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Total de ingresos')
    ax.set_title('Variación de Ingresos por Fecha')

    # Ajustar las etiquetas del eje x para mostrar todas las fechas
    ax.set_xticks(fechas_num)
    ax.set_xticklabels(fechas, rotation=45, ha='right')

    ax.legend()

    # Guardar la figura en un objeto BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)

    # Convertir la imagen en base64
    img_ingresos = base64.b64encode(img_buf.read()).decode('utf-8')

    # Cerrar la conexión y la figura para liberar recursos
    conn.close()
    plt.close()

    return img_ingresos



def registro_directo(placa, hora_entrada, direccion):
    crear_tabla()
    
    # Conectar a la base de datos y agregar un nuevo registro
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estacionamiento (fecha, hora, tipo, rol, direccion)) VALUES (?, ?, ?, "ingreso")', (placa, hora_entrada, direccion))
    conn.commit()
    conn.close()

def imagen_NOSE():
    conn = sqlite3.connect(DATABASE)
    query = "SELECT fecha, hora, tipo, direccion FROM estacionamiento"
    df = pd.read_sql_query(query, conn)
    print("************************",df)

    # Combinar la columna 'fecha' y 'hora' y convertirla a un objeto datetime
    df['Fecha_Hora'] = pd.to_datetime(df['fecha'] + ' ' + df['hora'])
    
    print(df['Fecha_Hora'])

    # Filtrar por ingresos y egresos
    ingresos = df[df['direccion'] == 'ingreso']
    egresos = df[df['direccion'] == 'egreso']
    print("ingresos",ingresos)
    print("egresos",egresos)
    # Agrupar por hora y contar el número de eventos por hora
    ingresos_por_hora = ingresos.groupby(ingresos['Fecha_Hora'].dt.hour)['direccion'].count()
    egresos_por_hora = egresos.groupby(egresos['Fecha_Hora'].dt.hour)['direccion'].count()
    print(df.dtypes)

    # Calcular la variación del contador por hora (ingresos - egresos)
    variacion_por_hora = ingresos_por_hora - egresos_por_hora
    print(variacion_por_hora,"ingresos por hora")

    # Graficar la variación del contador por hora
    plt.figure(figsize=(10, 6))
    variacion_por_hora.plot(marker='o', linestyle='-', color='b')
    plt.title('Variación del Contador por Hora')
    plt.xlabel('Hora del Suceso')
    plt.ylabel('Variación del Contador')
    plt.grid(True)
    plt.show()


    # Cerrar la conexión a la base de datos
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
    # enviar_actualizacion()


# registrar_entrada('grande', 'catedratico', 'ingreso')
# registrar_entrada('pequeño', 'estudiante', 'ingreso')
# registrar_entrada('mediano', 'ajeno', 'ingreso')
# imagen_NOSE()


# Nueva ruta para limpiar la base de datos
@app.route('/limpiar_base_de_datos')
def limpiar_base_de_datos():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estacionamiento')
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/seleccionar_fechas', methods=['GET', 'POST'])
def seleccionar_fechas():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        # Realizar acciones con las fechas, como hacer la petición a la API

        return redirect(url_for('grafica_barras_rol', fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))

    return render_template('seleccionar_fechas.html')


@app.route('/eliminar_base_de_datos')
def eliminar_base_de_datos():
    try:
        os.remove(DATABASE)
        return "Base de datos eliminada exitosamente."
    except FileNotFoundError:
        return "La base de datos no existe."
    

if __name__ == '__main__':
    socketio.run(app, debug=True)
