import unittest
import socket
import os
import pickle
from agentPi import agentPi_client.py as ap

class TestConsole(unittest.TestCase):
    
    def setUp(self):
        username = "Punita"
        password = "TestPass"
        CARID = '1001'
        MAKEBRAND = 'Mercedes'
        BODYTYPE = 'SEDAN'
        COLORTYPE = 'BLACK'
        NUMSEATS = 5
        HOURLYCOST = 50.00
        pass
        
    def testLogin(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            sendmsgTest = ("{},{},{}".format(username, password, CARID))
            s.sendall(sendmsg.encode())
            dataTest = s.recv(4096)
            
        self.assertEqual(ap.login().data, dataTest)
        
    def testCarDetails(self):
        ap.CARID = CARID
        ap.MAKEBRAND = MAKEBRAND
        ap.BODYTYPE = BODYTYPE
        ap.COLORTYPE = COLORTYPE
        ap.NUMSEATS = NUMSEATS
        ap.HOURLYCOST = HOURLYCOST
        
        ap.enterCarDetails()
        
         with open(testCarDetail, 'wb') as testF:
             pickle.dump([CARID,MAKEBRAND,BODYTYPE,COLORTYPE,NUMSEATS,HOURLYCOST],testF)
             
        self.assertEqual(ap.enterCarDetails().f, testF)
        
