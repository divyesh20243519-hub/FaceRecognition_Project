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

with open('names.pkl','rb') as f:
    LABELS = pickle.load(f)
with open('faces_data.pkl','rb') as f:
        FACES=pickle.load(f)


knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,LABELS)

# ADDED: distance threshold for the "UNKNOWN" check. KNN by default always predicts
# the closest matching label, even for a face it's never seen before -- there's no
# built-in concept of "none of these match well enough". This threshold is the max
# Euclidean distance (in raw flattened-pixel space) allowed before we treat a face as
# unrecognized instead of trusting the nearest match.
# NOTE: this needs to be tuned empirically for your setup (camera, lighting, dataset
# size) -- print `nearest_distance` for a few known and unknown faces first, then set
# the threshold roughly halfway between the typical "known" distances and "unknown" ones.
UNKNOWN_DISTANCE_THRESHOLD = 25000

COL_NAMES = ['Name' , 'Date' , 'Time']

# ADDED: checks whether a person has already been logged in today's attendance file,
# so pressing 'O' repeatedly for the same person doesn't create duplicate rows.
def already_marked_today(file_path, name):
    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header row
        for row in reader:
            if row and row[0] == name:
                return True
    return False

# CHANGED (optimization): background image is now loaded ONCE before the loop instead
# of being re-read from disk on every single frame (~30x/sec). Disk I/O inside a hot
# loop is unnecessary work when the image never changes -- this alone meaningfully cuts
# per-frame overhead with a one-line move, no logic change.
imgBackground = cv2.imread('../background.png')
if imgBackground is None:  # ADDED: fail loudly and immediately instead of crashing
    raise FileNotFoundError("Could not load '../background.png' -- check the path.")

attendence = None  # ADDED: initialized before the loop so it's never undefined

while True:

    ret,frame=video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray,1.3,5)

    BOX_COLOUR = (80, 220, 100) 

    for (x,y,w,h) in faces:
        crop_img = frame[y:y+h , x:x+w]
        resized_img = cv2.resize(crop_img,(250,250)).flatten().reshape(1,-1)
        # we flatten and reshape to make it 2D as required by the KNN model.

        # CHANGED: was knn.predict(resized_img) -- now we also pull the actual
        # distance to the nearest neighbor via kneighbors(), so we can tell the
        # difference between "confidently recognized" and "closest match, but not
        # close enough to trust".
        distances, _ = knn.kneighbors(resized_img, n_neighbors=1)
        nearest_distance = distances[0][0]

        if nearest_distance > UNKNOWN_DISTANCE_THRESHOLD:
            output = ["UNKNOWN"]
        else:
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
         # ADDED: guard against marking attendance when no face was ever detected --
         # previously `attendence` could be undefined here and crash, or silently
         # reuse a stale value from a much earlier frame.
         if attendence is None:
              speak("No face detected")
         elif attendence[0] == "UNKNOWN":  # ADDED: don't log unrecognized faces as attendance
              speak("Face not recognized")
         elif exist and already_marked_today(file_path, attendence[0]):  # ADDED: duplicate check
              speak("Already marked")
         else:
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
