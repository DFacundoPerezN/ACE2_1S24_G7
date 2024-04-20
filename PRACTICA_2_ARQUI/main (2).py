import cv2
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.SerialModule import SerialObject
import time

arduino = SerialObject('COM6')
cap = cv2.VideoCapture(0)
detector = FaceDetector()



caras = []
contador = 0
while True:
    success, img = cap.read()

    img, bBoxes = detector.findFaces(img)
    file = open("contador.txt","r")
    datos_previos = int(file.read().strip())
    
    if len(bBoxes) > 0:
        score = bBoxes[0]['score'][0]
        if score > 0.9:
            arduino.sendData([1,0, 1, 0])
            contador =datos_previos+1
            print(contador)
            face = "VERDADERO"
            cv2.putText(img, f'CARA DETECTADA: {(face)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0), 2)
            file = open("contador.txt","w")
            file.write(str(contador))
            file.close()
            time.sleep(1)
        elif score <0.9 :
            arduino.sendData([0,1, 0, 1])
            face = "FALSO"
            cv2.putText(img, f'CARA DETECTADA: {(face)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0), 2)
            time.sleep(4)
    else:
        arduino.sendData([0,1, 0, 1])
        face = "FALSO"
        cv2.putText(img, f'CARA DETECTADA: {(face)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0), 2)
        time.sleep(4)

    

        
    cv2.imshow("Video", img)
    cv2.waitKey(1)
sock.close()