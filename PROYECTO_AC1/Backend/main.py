import serial        
import time
import argparse


class DbInfo:
    def __init__(self,size="",rol="",direction=""):
        self.size = size
        self.rol = rol
        self.direction = direction


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
     
     information = information.decode('utf-8').strip('\n').strip('\r').split(":")
     print(information)
     
     if "Habitacion1" in information:
         rows = information[1].split(";")
         for i,position in zip(range(len(rows[0].split(","))),rows[0].split(",")):
             if position == "1":
                 print(f"Se encontro persona en 0,{i}")
            
             else:
                continue
        
         for i,position in zip(range(len(rows[1].split(","))),rows[1].split(",")):
             if position == "1":
                 print(f"Se encontro persona en 1,{i}")
            
             else:
                 continue
        
         for i,position in zip(range(len(rows[2].split(","))),rows[2].split(",")):
             if position == "1":
                 print(f"Se encontro persona en 2,{i}")
            
             else:
                 continue
        
         for i,position in zip(range(len(rows[3].split(","))),rows[3].split(",")):
             if position == "1":
                 print(f"Se encontro persona en 3,{i}")
            
             else:
                 continue
                    
    
    
                              
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
     






