import unittest
import cv2
from pyzbar import pyzbar
from QrScan.py import QrScan as scanner

class TestScanner(unittest.TestCase):

    def setUp(self):
        testImg = cv2.imread('Codes/frame.png')
        pass
        
    def test_decode(self):
        testImg1 = cv2.imread('Codes/frame.png')
        actualCode = scanner.scan().codes
        expectedCode = pyzbar.decode(testImg1)
        self.assertEqual(actualCode, expectedCode)
        
    def test_scan(self):
        testImg2 = cv2.imread('Codes/frame.png')
        testCode = pyzbar.decode(testImg2)
        actualCodeData = scanner.scan().codeData
        actualCodeType = scanner.scan().codeType
        expectedCodeData = testCode.data.decode("utf-8")
        expectedCodeType = testCode.type
        self.assertEqual(actualCodeData, expectedCodeData)
        self.assertEqual(actualCodeType, expectedCodeType)
        
 