from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-e", "--encodings", default="encodings.pickle",
#help="path to serialized db of facial encodings")
#ap.add_argument("-r", "--resolution", type=int, default=240,
#    help="Resolution of the video feed")
#ap.add_argument("-d", "--detection-method", type=str, default="hog",
#    help="face detection model to use: either `hog` or `cnn`")
#args = vars(ap.parse_args())

class FaceRecognizer:
    def RecognizeFaces():
        #Define models for recognition
        faceCas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        #font = cv2.FONT_HERSHEY_SIMPLEX

        

        #init ID counter
        id = 0

        # load the known faces and embeddings
        print("Loading Encodings...")
        encodingData = pickle.loads(open('encodings.pickle', "rb").read())

        for (i,imgPath) in imgPaths:
            
            #load input img and convert to grayscale
            img = cv2.imread(imgPath)
            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
        #    faces = face_cascade.detectMultiScale(grayImg, 1.3, 5)
            
            print("[INFO] Recognizing faces...")
            
            #detect x,y coordinates of bounding boxes for each face
            boxes = face_recognition.face_locations(grayImg, model="hog")
            
            #compute unique encodings for each face
            encodings = face_recognition.face_encodings(grayImg, boxes)
            
            # initialize the list of names for each face detected
            names = []
            
            for encoding in encodings:
                matches = face_recognition.compare_faces(encodingData["encodings"], encoding)
        #        matches = face_recognition.compare_faces(encodingData, encoding)
                name = "Unknown"
                
                if True in matches:
                    # Find indexs of matched faces
                    matchedIndexs = [i for (i, b) in enumerate(matches) if b]
                    
                    # Initialize dictionary to count times faces matched
                    counts = {}
                    
                    # loop over matched indexs and maintain count for recognized faces
                    for i in matchedIndexs:
                        name = encodingData["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                        
                    #Get name of face with most counts
                    name = max(counts, key=counts.get)
                
                #Add name to list of names
                names.append(name)
                
#                return name;
            
            for ((top, right, bottom, left), name) in zip(boxes, names):
                #Draw rectangle around face
                cv2.rectangle(img, (left, top), (right, bottom), (0,255,0), 2)
                
                #Calculate where to display name
                y = top - 15 if top - 15 > 15 else top + 15
                
                cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
                
        cv2.imshow("Image", img)
        
        return name;
        
    



