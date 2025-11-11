import cv2
import pickle # this helps to save the data in binary format    
import numpy as np
import os
# CascadeClassifier is used to detect the face
# VideoCapture is used to capture video from the camera
# 5 min neighbours -> minimum 5 objects/faces should be detected to consider it as a face
# haarcascase is a pre-trained model to detect faces

video = cv2.VideoCapture(0) # the 0 means default camera
facedetect = cv2.CascadeClassifier('C:/Users/divye/OneDrive/Desktop/FaceRecognitionProject/Data/haarcascade_frontalface_default.xml')

faces_data = [] # list to store the faces
i = 0

while True:

    if len(faces_data) >= 100: # dont need AGAIN !
        break
    ret,frame=video.read() # frame read or not ? ret = True/False
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # convert the frame to grayscale
    faces = facedetect.detectMultiScale(gray,1.3,5) # detect the faces in the frame

    # 1.3 and 5 are parameters for the detectMultiScale function
    # 1.3 is the scale factor in easy words is how much the image size is reduced at each image scale
    # 5 is the minNeighbours which means how many neighbours each rectangle should have to retain
        
    for (x,y,w,h) in faces:  # for each face detected at coordinates (x,y) with width w and height h
        cv2.rectangle(frame,(x,y),(x+w+10,y+h+10),(0,255,0),2) # draw rectangle around the face
        face = frame[y:y+h+10,x:x+w+10 , :]  # crop the face from the frame
        face = cv2.resize(face,(250,250))
        if len(faces_data)<100:  # store only 100 faces
            faces_data.append(face)  # add the face to the list
        i  += 1
        cv2.putText(frame,str(len(faces_data)),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3) # display the number of faces collected
        cv2.rectangle(frame,(x,y),(x+w+10,y+h+10),(0,255,0),2)
        cv2.imwrite("Data/Faces/user."+str(len(faces))+'.jpg',face) # save the face in the Data/faces folder
        
    cv2.imshow("My Face - PRESS 'q' to quit.",frame)
    k=cv2.waitKey(30)  # wait for 10 ms for a key press
    if k == ord('q') or len(faces_data) >= 100:
        break
    
video.release()  # release the camera (free the camera)
cv2.destroyAllWindows()  # cloes all the windows opened by OpenCV

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(faces_data.shape[0],-1) # CHANGE 4D -> 2D.
# the reshape(faces_data.shape[0],-1) means that we want to keep the number of rows same and we want to flatten the columns
# the -1 means that we want to flatten the columns
# originally faces_data is of shape (100,250,250,3) 0 images of size 250x250 with 3 color channels 
# after reshape it becomes (100,187500) 100 images of size 187500 (250*250*3)

name = input("Enter the name of the person : ")

# create a names list of size 100 
# cause thats how many pictures are taken for each person
# if already list hai , then 
# concatenate

if 'names.pk1' not in os.listdir('Data/'):
    names = [name]*100
    with open('Data/names.pk1','wb') as f:  # wb means write binary
        pickle.dump(names,f)  # dump the list in the file
else:
    # --- IF FILE ALREADY EXISTS ----
    with open('Data/names.pk1','rb') as f:
        names = pickle.load(f)

    names = names + [name]*100 # append to the list  
    
    # SAVE IT BACK.
    with open('Data/names.pk1','wb') as f:
        pickle.dump(names, f)

# same code but now we hold the pixels and pattern for every face
# 2D NumPy array where each row stores information on ONE PICTURE
# same faces are GROUPED TOGETHER SEQUENTIALLY
# eg:
# Row(0->99) is for divyesh
# Row(100->199) is for tanu

if 'faces_data.pk1' not in os.listdir('Data/'):
    with open('Data/faces_data.pk1','wb') as f:  # wb means write binary
        pickle.dump(faces_data,f)  # dump an empty list if the file does not exist
else:
    with open('data/faces_data.pk1','rb') as f:
        faces = pickle.load(f)

    faces=np.append(faces,faces_data,axis=0)
    
    # SAVE IT BACK.
    with open('data/faces_data.pk1','wb') as f:
        pickle.dump(faces,f)

# *************************** STEP 1 COMPLETE ************************

# names.pk1 has the labels
# faces_data.pk1 has the face data in flattened format