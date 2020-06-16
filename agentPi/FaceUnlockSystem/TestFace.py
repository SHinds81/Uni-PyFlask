import unittest
import cv2
from FaceUnlockSystem import FaceTrainer.py as ft
from FaceUnlockSystem import FaceRecognizer.py as fr

class TestFaceTrainer(unittest.TestCase):

    def setUp(self):
        encodingData = pickle.loads(open('encodings.pickle', "rb").read())
        imgPaths=list(paths.list_images('faces/'))
        testImg = cv2.imread(imgPaths)
        pass
        
    def test_image_search(self):
        actualImg = fr.RecognizeFaces().img
        expectedImg = testImg
        self.assertEqual(actualImg, expectedImg)
        
    def test_image_grey(self):
        actualImg = fr.RecognizeFaces().grayImg
        expectedImg = cv2.cvtColor(testImg, cv2.COLOR_BGR2GRAY)
        self.assertEqual(actualImg, expectedImg)
        
    def test_faces_trained(self):
        self.assertEqual(ft.TrainFaces(), encodingData)
        
    def test_faces_recognized(self):
        self.assertEqual(fr.RecognizeFaces(), encodingData["names"])
        
        
