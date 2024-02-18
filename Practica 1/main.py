import serial        
import time

serialArduino = serial.Serial("COM3",9600,timeout=1.0)
#timeout (1 segundo) o tiempo máximo de espera para una lectura.
time.sleep(1) # espera 1 seg, para dar tiempoa conectarse

direccion="NONE"
tipo ="desconocido"
rol="ajeno"

while True:
     #cad =serialArduino.readline().decode('ascii') 

     cad =serialArduino.readline().decode('ascii').strip()
     parts = cad.split(";")
     tipo = parts[0]
     rol = parts[1]
     direccion = parts[2]

    #  if cad:         
    #      pos=cad.index(":")
    #      label=cad[:pos]
    #      value=cad[pos+1:]
    #      if label == 'dis':
    #          print("Es val de la distancia es: {}".format(value))
    #      if label == 'pot':
    #          print("Es valor del potenciometro es: {}".format(value))     
    #      print("**************")
     







