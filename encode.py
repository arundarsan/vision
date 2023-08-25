import os
import pickle
import face_recognition
import cv2
participantfolderPath = 'resources'
participantknownPersonListPath = os.listdir(participantfolderPath)
participantknownPersonList = []
participantIds = []
for path in participantknownPersonListPath:
   participantknownPersonList.append(cv2.imread(os.path.join(participantfolderPath,path)))
   participantIds.append(os.path.splitext(path)[0])
def findencording(participantknownPersonList):
    encodeList = []
    for img in participantknownPersonList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
print("Start Encording.......")
encodeListKnown = findencording(participantknownPersonList)
print("Complete Encording......5")
encodeListKnownWithIds = [encodeListKnown,participantIds ]
file  = open("encoding.p",'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("file saved")


