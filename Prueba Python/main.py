import serial,time

ser = serial.Serial('COM3',9600)

data = ser.readline().decode('utf-8')

print(data)

ser.close()