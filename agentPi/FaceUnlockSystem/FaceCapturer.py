#Program to train Pi to detect faces

import cv2
import numpy as np
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required = True,
    help="The name/id of this person you are recording")
ap.add_argument("-i", "--dataset", default = "dataset",
    help="path to input directory of faces + images")
args = vars(ap.parse_args())

# use name as folder name
name = args["name"]
folder = "./dataset/{}".format(name)

# Create a new folder for the new name
if not os.path.exists(folder):
    os.makedirs(folder)

#Code to display video stream from Pi
capture = cv2.VideoCapture(0)
capture.set(3,640)  #width
capture.set(4,480)  #height

#Load Classifier
faceDetector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

# user_id = input('\n Enter Username')
print("\n Starting Capture. Please look at camera")

count=0
while True:
    ret, img = capture.read()
    img = cv2.flip(img,-1)
    grayInput = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   #converts image to grayscale

    #Classifier function called with parameters
    faces = faceDetector.detectMultiScale(
        grayInput,
        scaleFactor=1.3,
        minNeighbors=5,
    )

    #mark position of faces in image, and display rectangle on them
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        count = count+1

        #Save image to dataset folder
        img_name = "{}/{:04}.jpg".format(folder, count)
        cv2.imwrite(img_name, grayInput[y:y+h,x:x+w])
        print("{} written!".format(img_name))
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 30: #Stop video once 30 samples taken
         break

print("\n Exiting Program")
capture.release()
cv2.destroyAllWindows()
