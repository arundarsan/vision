import os
import pickle
import face_recognition
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : 'https://face-recognition-36ef1-default-rtdb.firebaseio.com',
    'storageBucket' : 'face-recognition-36ef1.appspot.com'
    })
studentfolderPath = 'resources'
studentknownPersonListPath = os.listdir(studentfolderPath)
print(studentknownPersonListPath)
studentknownPersonList = []
studentIds = []
for path in studentknownPersonListPath:
   studentknownPersonList.append(cv2.imread(os.path.join(studentfolderPath,path)))
   studentIds.append(os.path.splitext(path)[0])
#print(studentknownPersonList)
#print(studentIds)
   fileName = f'{studentfolderPath}/{path}'
   bucket = storage.bucket()
   blob = bucket.blob(fileName)
   blob.upload_from_filename(fileName)
def findencording(studentknownPersonList):
    encodeList = []
    print(encodeList)
    for img in studentknownPersonList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       # print(img)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        print(encodeList)
    return encodeList



print("Start Encording.......")
print(studentknownPersonList)
encodeListKnown = findencording(studentknownPersonList)
print("Complete Encording......5")
print(encodeListKnown)


encodeListKnownWithIds = [encodeListKnown,studentIds ]

file  = open("encoding.p",'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("file saved")


