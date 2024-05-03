import cv2
import face_recognition
import pickle
import os
#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import db
#from firebase_admin import  storage

#cred = credentials.Certificate("serviceAccountKey.json")
#firebase_admin.initialize_app(cred, {
#    'databaseURL': "",
#    'storageBucket': ""
#})


folderPath = 'Cara'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
rostros = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    rostros.append(os.path.splitext(path)[0])

    #fileName = f'{folderPath}/{path}'
    #bucket = storage.bucket()
    #blob = bucket.blob(fileName)
    #blob.upload_from_filename(fileName)


    # print(path)
    print(os.path.splitext(path)[0])
print(rostros)


def findEncodings(listaimg):
    encodeList = []
    for img in listaimg:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
listaCarasConocidas = findEncodings(imgList)
listaCarasConocidasconID = [listaCarasConocidas, rostros]
print("Encoding Complete")

file = open("RegistroRostro.p", 'wb')
pickle.dump(listaCarasConocidasconID, file)
file.close()
print("File Saved")