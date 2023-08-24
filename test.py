#!/usr/bin/env python
from __future__ import print_function
import os
import rospy
import cv2
import threading
import pickle
import face_recognition
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from qt_nuitrack_app.msg import Faces, FaceInfo
import numpy as np
import cvzone
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials
import firebase_admin
from std_msgs.msg import String
from qt_robot_interface.srv import *
from qt_gesture_controller.srv import *
#cred = credentials.Certificate("serviceAccountKey.json")
#firebase_admin.initialize_app(cred , {
#    'databaseURL' : 'https://face-recognition-36ef1-default-rtdb.firebaseio.com',
#    'storageBucket' : 'face-recognition-36ef1.appspot.com'
 #   })


class image_converter:
   def __init__(self):
        self.faces = None
        self.say_once = 1
        self.say_false = 1
        self.face_time = None
        self.folderPath = 'resources'
        self.knownPersonListPath = os.listdir(self.folderPath)
        self.knownPersonList = []
        for self.path in self.knownPersonListPath:
            self.knownPersonList.append(cv2.imread(os.path.join(self.folderPath,self.path)))
        file = open("encoding.p" , 'rb')
        self.encodeListKnownWithIds = pickle.load(file)
        self.encodeListKnown, self.studentIds = self.encodeListKnownWithIds
        file.close()
        self.pub = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size=10)
        rate = rospy.Rate(10)
        self.lock = threading.Lock()
        self.bridge = CvBridge()
        print('bridge')
        self.image_pub = rospy.Publisher("/face_recognition/out", Image, queue_size=1)
        #print('face_eco')
        self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image, self.image_callback)
        print('cameraraw')
        #self.face_sub = rospy.Subscriber("/qt_nuitrack_app/faces", Faces, self.face_callback)
        #print('nuitrack')
        self.audioPlay_pub = rospy.Publisher('/qt_robot/audio/play', String, queue_size=10)
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred , {
            'databaseURL' : 'https://face-recognition-36ef1-default-rtdb.firebaseio.com',
            'storageBucket' : 'face-recognition-36ef1.appspot.com'
                })


   def face_callback(self, data):
        print("face_callback")
        self.lock.acquire()
        self.faces = data.faces
        self.face_time = rospy.Time.now()
        self.lock.release()

   def image_callback(self,data):
        try:
            id = 0 
            counter = 0
            #camera = cv2.VideoCapture(0)
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            #self.image_sub.publish(cv_image)
            #cv2.imshow("camera_feed", cv_image) 
            cv2.imwrite("3efilename.jpg", cv_image)
            ImgL = cv2.resize(cv_image, (0,0), None, 2, 2)
            Imgs = cv2.resize(cv_image, (0,0), None, 0.25, 0.25)
            cv2.imwrite("5quarter.jpg", Imgs)
            Imgs = cv2.cvtColor(Imgs, cv2.COLOR_BGR2RGB)
            cv2.imwrite("5bgr2rgb.jpg", ImgL)
            #FaceCurFramet = ""
            FaceCurFramet = face_recognition.face_locations(Imgs)
            print(FaceCurFramet)
            encode_current_face = face_recognition.face_encodings(Imgs, FaceCurFramet)
            print(encode_current_face)
            for encode_face, faceLoc in zip(encode_current_face,FaceCurFramet):
                matches = face_recognition.compare_faces(self.encodeListKnown, encode_face)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encode_face)
                print("matches", matches)
                print("faceDis",faceDis )
                if True not in  matches:
                       if self.say_false == 1:
                         self.pub.publish("Hi you are  not authenticated")
                         self.say_false += 1

                matchIndex = np.argmin(faceDis)
                print(matchIndex)
                if matches[matchIndex]:
                  y1, x2, y2, x1 = faceLoc
                  y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                  bbox= x1, y1, x2, y2
                  imgbackground = cvzone.cornerRect(ImgL, bbox, rt=0)
                  self.id = self.studentIds[matchIndex]
                  #cv2.imshow("Attendance", imgbackground)

                  cv2.imwrite("filepici.jpg", imgbackground)
                  print("sssss")
                  if counter == 0:
                      counter =1
            if counter !=0:
                if counter == 1:
                    print(self.id)
                    studentInfo = db.reference('database-1/{}'.format(self.id)).get()
                    print(studentInfo)
                    print(studentInfo['name'])
                    #cv2.putText(imgbackground, str(studentInfo['name']), (x1,y1), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    #self.audioPlay_pub.publish("Hello,{}".format(studentInfo['name']))
                    if  self.say_once == 1:
                       self.pub.publish("Hi {} you are authenticated".format(studentInfo['name']))
                       self.say_once += 1
                    else:
                       pass

        except CvBridgeError as e:
            print("error")
            print(e)
        #cv2.imshow("camera_feed", self.cv2_image) 

        (rows, cols, channels) = cv_image.shape
        self.lock.acquire()
        new_faces = self.faces
        new_face_time = self.face_time
        self.lock.release()

        if new_faces and (rospy.Time.now()-new_face_time) < rospy.Duration(5.0):
            for face in new_faces:
                rect = face.rectangle
                cv2.rectangle(cv_image, (int(rect[0]*cols),int(rect[1]*rows)),
                                      (int(rect[0]*cols+rect[2]*cols), int(rect[1]*rows+rect[3]*rows)), (0,255,0), 2)
                x = int(rect[0]*cols)
                y = int(rect[1]*rows)
                w = int(rect[2]*cols)
                h = int(rect[3]*rows)
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)


if __name__ == '__main__':
    print("test1")
    rospy.init_node('qt_face_recognition', anonymous=True)
    print("test2")
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
