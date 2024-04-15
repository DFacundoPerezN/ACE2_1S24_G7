import serial        
import time
import argparse
from probador import registrar_entrada

class DbInfo:
    def __init__(self,size="",rol="",direction=""):
        self.size = size
        self.rol = rol
        self.direction = direction

def printColor(colorines,direccion,tamanio):
    
     if((int(colorines[2])-int(colorines[0]))>30 and int(colorines[2])>int(colorines[1])):
          print("azul")
          registrar_entrada(tamanio,"trabajadores",direccion)
          
     elif((int(colorines[0])-int(colorines[1]))>9 and (int(colorines[0])-int(colorines[2]))>12):
          print("rojo")
          registrar_entrada(tamanio,"estudiante",direccion)
     elif(int(colorines[1])>50 and int(colorines[1])>int(colorines[2]) and abs(int(colorines[1])-int(colorines[0]))<25):
          print("amarillo")
          registrar_entrada(tamanio,"catedratico",direccion)
     else:
          print("otro")
          registrar_entrada(tamanio,"ajeno",direccion)

serialArduino = serial.Serial("COM3",9600,)
#timeout (1 segundo) o tiempo máximo de espera para una lectura.
time.sleep(1) # espera 1 seg, para dar tiempoa conectarse
contador = 0
# direccion="NONE"
# tipo ="desconocido"
# rol="ajeno"

while True:
     
     registroDB = DbInfo()
     tamanio = 0
     #cad =serialArduino.readline().decode('ascii') 

     information =serialArduino.readline()
     
     information = information.decode('utf-8').strip('\n').strip('\r').split()
     #print(information)
     if "DR" in information[0]:
          if "entrando" in information[0]:
               print("Deteccion de entrada exitosa")
               if "PR" in information[1]:
                    print(information[1])
                    distancia = information[1].split("=")
                    if int(distancia[1]) >= 0 and int(distancia[1]) <= 2:
                         print("GRANDE")
                         tamanio = "grande"
                    elif int(distancia[1]) >= 3 and int(distancia[1]) <=4:
                         print("MEDIANO")
                         tamanio = "mediano"
                    elif int(distancia[1]) >= 5:
                         print("PEQUEÑO")
                         tamanio = "pequeño"
                    if "RGB" in information[2]:
                         #print(information[2])
                         colorines = information[2].split("=")
                         #print(colorines)
                         colorines = colorines[1].split(",")
                         print(colorines)
                         printColor(colorines,"ingreso",tamanio)
                              
          elif "saliendo" in information[0]:
               print("Deteccion de salida exitosa")
               if "PR" in information[1]:
                    print(information[1])
                    distancia = information[1].split("=")
                    if int(distancia[1]) >= 0 and int(distancia[1]) <= 2:
                         print("GRANDE")
                         tamanio = "grande"
                    elif int(distancia[1]) >= 3 and int(distancia[1]) <=5:
                         print("MEDIANO")
                         tamanio = "mediano"
                    elif int(distancia[1]) >= 6:
                         print("PEQUEÑO")
                         tamanio = "pequeño"
                    if "RGB" in information[2]:
                         #print(information[2])
                         colorines = information[2].split("=")
                         #print(colorines)
                         colorines = colorines[1].split(",")
                         print(colorines)
                         printColor(colorines,"egreso",tamanio)
                              
serialArduino.close()


    #  if cad:         
    #      pos=cad.index(":")
    #      label=cad[:pos]
    #      value=cad[pos+1:]
    #      if label == 'dis':
    #          print("Es val de la distancia es: {}".format(value))
    #      if label == 'pot':
    #          print("Es valor del potenciometro es: {}".format(value))     
    #      print("**************")
     






