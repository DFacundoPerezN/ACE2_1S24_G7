import serial        
import time
import argparse


serialArduino = serial.Serial("COM3",9600,)
#timeout (1 segundo) o tiempo máximo de espera para una lectura.
time.sleep(1) # espera 1 seg, para dar tiempoa conectarse
contador = 0
# direccion="NONE"
# tipo ="desconocido"
# rol="ajeno"

while True:
     #cad =serialArduino.readline().decode('ascii') 

     information =serialArduino.readline()
     
     # if "UP" in information:
     #      print("arriba")
     # elif "LEFT" in information:
     #      print("Direccion invalida")
     # elif "RIGHT" in information:
     #      print("Direccion invalida")
     # elif "DOWN" in information:
     #      print("abajo")
     
     #print(information)
     
     information = information.decode('utf-8').strip('\n').strip('\r').split(' ')
     
     print(information)

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
     







