import cv2
from cvzone.FaceDetectionModule import FaceDetector
import time
import pickle
import face_recognition
import cvzone
import numpy as np
import serial
import meet
import datetime
import mysql.connector
from mysql.connector import Error
#from datetime import datetime
import sys

cap = cv2.VideoCapture(1)
detector = FaceDetector()
meetOpen = True
meetClose = True
information = 0
#arduino = serial.Serial('COM6', 9600,)
time.sleep(1)

print("Cargando Base de Datos ...")
file = open('RegistroRostro.p', 'rb')
listaCarasConocidasconID = pickle.load(file)
file.close()
listaCarasConocidas, rostros = listaCarasConocidasconID
# print(rostros)
print("Datos Cargados")

file = open("x.txt","r")
file = open("y.txt","r")
file = open("w.txt","r")
file = open("h.txt","r")
while True:
    success, img = cap.read()
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    '''
    information =arduino.readline()
    information = information.decode('utf-8')
    print(information)
    '''



    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(listaCarasConocidas, encodeFace)
            faceDis = face_recognition.face_distance(listaCarasConocidas, encodeFace)
            print("matches", matches)
            print("faceDis", faceDis)
            
            

            matchIndex = np.argmin(faceDis)
            #print("Match Index", matchIndex)
            tiempo_in = []

            

            if matches[0]:
                print("Ingeniera Diana Detectada")
                fecha_inicio = datetime.datetime.now()
                tiempo_in.append(fecha_inicio)
                #arduino.sendData([1,0, 1, 0])
                y1, x2, y2, x1 = faceLoc
                bbox = x1, y1, x2 - x1, y2 - y1
                facebox = x1, y1, x2, y2
                img = cvzone.cornerRect(img, bbox, rt=0)
                cv2.putText(img, f'DIANA DETECTADA', (20, 70), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0), 2)
                id = rostros[matchIndex]
                
                
            


                if meetOpen:
                    meet.newMeet()
                    meetOpen = False
                '''
                for x1, y1, x2, y2 in faceCurFrame:
                    xc, yc = x1 + x2 / 2, y1 + y2 / 2
                    ih, iw, _ = img.shape
                    xcn, ycn = xc / iw, yc / ih,
                    wn, hn = x2 / iw, y2 / ih
                    print(xcn, ycn, wn, hn)
                    #sending coordinates to Arduino
                    string='X{0:d}Y{1:d}'.format(int(xcn+wn),int(ycn+hn))
                    print(string)
                    arduino.write(string.encode('utf-8'))
                    #for testing purpose
                    read= str(arduino.readline(arduino.inWaiting()))
                    time.sleep(0.05)
                    print('data from arduino:'+read)
                '''

                
                for y1,x2,y2,x1 in faceCurFrame:
                    print("x1:", x1)
                    print("y1:", y1)
                    print("x2:", x2)
                    print("y2:", y2)
                    print("coordendas"+str(faceLoc))

                    file = open("x.txt","w")
                    file.write(str(x1))
                    file.close()
                    file = open("w.txt","w")
                    file.write(str(x2))
                    file.close()
                    file = open("y.txt","w")
                    file.write(str(y1))
                    file.close()
                    file = open("h.txt","w")
                    file.write(str(y2))
                    file.close()
                    '''
                    #sending coordinates to Arduino
                    string='X{0:d}Y{1:d}'.format((x1+x2//2),(y1+y2//2))
                    print(string)
                    arduino.write(string.encode('utf-8'))
                    #for testing purpose
                    read= str(arduino.readline(arduino.inWaiting()))
                    time.sleep(0.05)
                    print('data from arduino:'+read)
                    '''
                
                with open("boton.txt", "r") as archivo:
                    contenido = archivo.read()

                print("ESTO ES CONTENIDO " + contenido)
                print("ESTO ES TIPO DE CONTENIDO" + str(type(contenido)))

                if "1" in contenido:
                    print("ENTRE")
                    print("HOLA MUNDO")
                    meet.closeMeet()
                    meetClose = False
                    login = tiempo_in[0]
                    logout = datetime.datetime.now()
                    mandar(logout)
                    time.sleep(3)
                    sys.exit()
                time.sleep(1)
                    
                
            elif matches[1]:
                print("Gabriel Detectado")
                #arduino.sendData([1,1, 1, 1])
                y1, x2, y2, x1 = faceLoc
                bbox = x1, y1, x2 - x1, y2 - y1
                img = cvzone.cornerRect(img, bbox, rt=0)
                cv2.putText(img, f'GABRIEL DETECTADO', (20, 70), cv2.FONT_HERSHEY_PLAIN,1, (0, 0, 255), 2)
                id = rostros[matchIndex]

            else:
                print("Rostro registrado no detectado")
                #arduino.sendData([0,1, 0, 1])
                cv2.putText(img, f'NO DETECTADO', (20, 70), cv2.FONT_HERSHEY_PLAIN,1, (255, 0, 0), 2)
                id = rostros[matchIndex]
        

    

        
    cv2.imshow("Video", img)
    cv2.waitKey(1)

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
            #now = datetime.now()
            #fecha_formateada = now.strftime("%Y-%m-%d")
            #hora_formateada = now.strftime("%H:%M:%S")
            hora_formateada=logout
            # Insertar un registro en la base de datos
            consulta = "INSERT INTO registros (logueado, fecha, hora) VALUES (%s, %s, %s)"
            cursor.execute(consulta, ("si", '2024-05-02', hora_formateada))
            conexion.commit()

        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
