#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

#AGENT PI

import socket
import os
import pickle
import time
from blutooth import search as bt
#from FaceUnlockSystem.FaceRecognizer import FaceRecognizer


#HOST = input("Enter IP address of server: ")
HOST = "127.0.0.1"
# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 65000         # The port used by the server.
ADDRESS = (HOST, PORT)


#Car Detail
CARID = '1001'
MAKEBRAND = 'Mercedes'
BODYTYPE = 'SEDAN'
COLORTYPE = 'BLACK'
NUMSEATS = "5"
HOURLYCOST = "50.00"


 
class AgentPi:
    """
    This class represents the AgentPi
    """
#    def __init__():
#        """
#        empty default Constructor
#        """
    
    def carDetails():
        """
        A method that prints the details of the car this Pi is attached to
    
        """
        
        print("Car id: "+CARID)
        print("Brand: "+MAKEBRAND)
        print("Body type: "+BODYTYPE)
        print("Color: "+COLORTYPE)
        print("# seats: "+NUMSEATS)
        print("Hourly cost: "+HOURLYCOST)
    

    def login(s):
        """
        Gets the login details of a user and sends username, password, car's id to the masterPi to be checked. if login is correct for this car unlock car
    
        :type s: socket
        :param s: socket connection to the masterPi 
        """
        
        username = input("Enter username: ")
        password = input("Enter password: ")
    
        sendmsg = ("{},{},{},{}".format("unlock",username, password, CARID))
        
        s.sendall(sendmsg.encode())
        data = s.recv(4096)
        print("Received {} bytes of data decoded to: '{}'".format(
                len(data), data.decode()))
        if data.decode() == 'true':
            print ("Welcome, car is unlocked. Full access granted")
        else:
            print("Car did not unlock. make sure your username and password are correct")

#   def enterCarDetails():
#    CARID=input("Car id: ")
#    MAKEBRAND=input("Brand: ")
#    BODYTYPE=input("Body type: ")
#    COLORTYPE=input("Color: ")
#    NUMSEATS=input("# seats: ")
#    HOURLYCOST=input("Hourly cost: ")
#    with open(carDetail, 'wb') as f:
#    pickle.dump([CARID,MAKEBRAND,BODYTYPE,COLORTYPE,NUMSEATS,HOURLYCOST],f)
    
    def returnCar(s):
        """
        logout the current user and notify the masterPi that the car has been returned
    
        :type s: socket
        :param s: socket connection to the masterPi 
        """
        username = input("Enter username: ")
        password = input("Enter password: ")
    
        sendmsg = ("{},{},{},{}".format("return",username, password, CARID))
        
        s.sendall(sendmsg.encode())
        data = s.recv(4096)
        if data.decode() == "true":

            sendmsg = ("{},{}".format("returnConfirm", CARID))
            s.sendall(sendmsg.encode())
            data = s.recv(4096)
            print("Received {} bytes of data decoded to: '{}'".format(
                    len(data), data.decode()))
            if data.decode() == 'success car returned':
                print("Car has been returned")
        else:
            print("Car could not be returned")
            
#    def faceLogin(s):
#        username = FaceRecognizer.RecognizeFaces()
#        sendmsg = ("{},{},{},".format("face",username,CARID))



    
    def connect():
        """
        if the agentPi can connect to the masterPi displays a menu of user options
        """
    
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Connecting to {}...".format(ADDRESS))
                s.connect(ADDRESS)
                print("Connected.")

                while True:
        
                    print ("*****MENU*****")
                    time.sleep(0.5)
                    print ("1: login")
                    print ("2: login with face Recognision")
                    print ("3: get car details")
                    print ("4: return car")
                    print ("5: Engineer login")
                    print ("6: quit")
        
                    entry = input("enrty: ")
        
                    if entry=='1':
                        AgentPi.login(s)
                    elif entry=='2':
                    #call face recognision
                        #AgentPi.faceLogin(s)
                        print("face")
                    elif entry=='3':
                        AgentPi.carDetails()
                    elif entry=='4':
                        AgentPi.returnCar(s)
                    elif entry=='5':
                        bool = bt()
                        if bool is True:
                            #Unlock car for engineer
                            print("Hello Engineer! Car is unlocked")
                        else:
                            print("Could not identify device. Try again")
                    elif entry=='6':
                        ##Run QR Code scanner
                        print('Scan QR Code')
                        
                    seif entry=='7':
                        break
                    else:
                        print ("entry unknown. please enter a number from the options above")
            
            message = "disconnect"
            s.sendall(message.encode())
            data = s.recv(4096)
            print("Received {} bytes of data decoded to: '{}'".format(
                    len(data), data.decode()))
    
            print("Disconnecting from server.")
            print("Done.")
            
        except socket.error:
            print("Caught exception socket.error")

    def main(self):
        """
        main method initialises the user menu choice and call connection method
        """
        while True:
            print("\n*****CAR.SHARE*****")
    #        if (CARID or MAKEBRAND or BODYTYPE or COLORTYPE == '') or (NUMSEATS or HOURLYCOST == 0):
    #            enterCarDetails()

            run = input("press enter to connect to server")
        
            if(run == ''):
                AgentPi.connect()


if __name__ == "__main__":
    ap = AgentPi()
    ap.main()
