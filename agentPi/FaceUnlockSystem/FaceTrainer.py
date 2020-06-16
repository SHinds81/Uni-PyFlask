import cv2
import argparse
import numpy as np
import os
import pickle
from imutils import paths
import face_recognition

class FaceTrainer:
    def TrainFaces():
        # construct the argument parser and parse the arguments
#        ap = argparse.ArgumentParser()
#        ap.add_argument("-i", "--dataset", default = "dataset",
#            help="path to input directory of faces + images")
#        ap.add_argument("-e", "--encodings", default = "encodings.pickle",
#            help="path to serialized db of facial encodings")
#        ap.add_argument("-d", "--detection-method", type = str, default = "hog",
#            help="face detection model to use: either `hog` or `cnn`")
#        args = vars(ap.parse_args())

        #Define models for recognition and detection
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')


        #Declare images path and create arrays for face samples and ids
        print("Quantifying faces...")
        imgPaths=list(paths.list_images('dataset/'))

        knownEncodings=[]
        knownNames=[]

        #For each image in  images path
        for (i,imgPath) in imgPaths:
            # newImg = Image.open(imgPath).convert('L')   #convert to grayscale
            # img_numpy = np.array(newImg,'uint8')


            # id = int(os.path.split(imgPath)[-1].split(".")[1])  #declare id for image
            # faces=detector.detectMultiScale(img_numpy)  #call detector for image

            # for(x,y,w,h) in faces:
            #     samples.append(img_numpy[y:y+h,x:x+w])  #mark position of face in sample
            #     ids.append(id)

            #extract name from img path
            print("Processing image {}/{}".format(i+1, len(imgPaths)))
            name = imgPath.split(os.path.sep)[-2]

            #load input image and convert to grayscale
            img = cv2.imread(imgPath)
            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            #detect x,y coordinates of bounding boxes for each face
            boxes = face_recognition.face_locations(grayImg, model = "hog")

            #compute unique encodings for each face
            encodings = face_recognition.face_encodings(grayImg, boxes)

            for encoding in encodings:
                #add new encoding and name to existing known set
                knownEncodings.append(encoding)
                knownNames.append(name)


        print("\n Getting encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}

        with open('encodings.pickle', "wb") as f:
            f.write(pickle.dumps(data))
            
        return data

    # faces,ids = getImageLabels(path)    #call detector method on dataset
    # recognizer.train(faces, np.array(ids))  #train recognizer with array of detected faces

    #Save trained model to new path
    # recognizer.write('trainer/trainresults.yml')

    # print("\n {0} faces trained. Exiting".format(len(np.unique(ids))))
