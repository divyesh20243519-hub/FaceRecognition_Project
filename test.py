from sklearn.neighbors import KNeighborsClassifier

import cv2 # Camera and Videos (2) 
import pickle # used for saving and loading files after opening and editing.
import numpy as np # used for numerical operations
import os # used for file operations
import csv # FOR ATTENDANCE (csv file)
import time # FOR TIMING
import datetime # FOR DATES

from win32com.client import Dispatch # helps to give voice output 

def speak(str1):
     speak=Dispatch("SAPI.SpVoice")
     speak.Speak(str1)


video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

with open('names.pk1','rb') as f:
    LABELS = pickle.load(f)
with open('faces_data.pk1','rb') as f:
        FACES=pickle.load(f)


knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,LABELS)

COL_NAMES = ['Name' , 'Date' , 'Time']

while True:

    ret,frame=video.read()
    imgBackground = cv2.imread('../background.png')
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray,1.3,5)

    BOX_COLOUR = (80, 220, 100) 

    for (x,y,w,h) in faces:
        crop_img = frame[y:y+h , x:x+w]
        resized_img = cv2.resize(crop_img,(250,250)).flatten().reshape(1,-1)
        # we flatten and reshape to make it 2D as required by the KNN model.
        output = knn.predict(resized_img)

        ts = time.time()
        dt = datetime.datetime.fromtimestamp(ts)
        date = dt.strftime("%Y-%m-%d")
        timestamp = dt.strftime("%H:%M:%S")

        # check if file exists first
        file_path = '../Attendance/Attendance_' + date + '.csv'
        exist=os.path.isfile(file_path)

        # Clean bounding box
        cv2.rectangle(frame, (x, y), (x+w, y+h), BOX_COLOUR, 2)

        # Filled label background above the box, sized to fit the name
        label = str(output[0])
        (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        cv2.rectangle(frame, (x, y - text_h - 15), (x + text_w + 10, y), BOX_COLOUR, -1)
        cv2.putText(frame, label, (x + 5, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        attendence = [output[0],date,timestamp]
    imgBackground[162 : 162+480 , 55 : 55+640]= frame
    cv2.imshow("Face Recognition System: ",imgBackground)
    k=cv2.waitKey(30)
    # for the ATTENDANCE WE USE 'O'
    if k==ord('O'):
         speak("Marked")
         time.sleep(1)
         if exist:
              with open(file_path,'a+',newline='') as f:
                   writer=csv.writer(f)
                   writer.writerow(attendence)
         else:
              with open(file_path,'a+',newline='') as f:
                   writer=csv.writer(f)
                   writer.writerow(COL_NAMES)
                   writer.writerow(attendence)
        
    # *** 'with open' automatically closes the file after the block is executed *** #
    if k == ord('Q'):  # FINSIHED WITH ATTENDANCE
          break
    
video.release()
cv2.destroyAllWindows()
