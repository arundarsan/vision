#!/usr/local/bin/python3
import cv2
import os
import face_recognition
import pickle 
import numpy as np
import cvzone
def createencoding():

folderPath = 'resources'
knownPersonListPath = os.listdir(folderPath)
knownPersonList = []
for path in knownPersonListPath:
   knownPersonList.append(cv2.imread(os.path.join(folderPath,path)))

print(type(knownPersonList))
    
file = open("encoding.p" , 'rb')
encodeListKnownWithIds = pickle.load(file)
print(encodeListKnownWithIds)
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
file.close()
cap =cv2.VideoCapture(0)
cap.set(3,640) 
while True:
    sucess, img = cap.read()
    Imgs = cv2.resize(img, (0,0), None, 0.25, 0.25)
    Imgs = cv2.cvtColor(Imgs, cv2.COLOR_BGR2RGB)
    faceCurFramet = face_recognition.face_locations(Imgs)
    encode_current_face = face_recognition.face_encodings(Imgs, faceCurFramet)
    for encode_face, faceLoc in zip(encode_current_face,faceCurFramet):
        matches =face_recognition.compare_faces(encodeListKnown, encode_face)
        faceDis = face_recognition.face_distance(encodeListKnown, encode_face)
        print("matches", matches)
        print("faceDis",faceDis )
        matchIndex = np.argmin(faceDis)
        print(matchIndex)
        
        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox= x1, y1, x2, y2
            imgbackground = cvzone.cornerRect(img, bbox, rt=0)
            cv2.imshow("Attendance", imgbackground)
            cv2.imwrite(filepic, imgbackground)
            print("sssss")

if __name__ == '__main__':
    #createencoding()