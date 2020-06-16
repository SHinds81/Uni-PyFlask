import socket
#from flask import json
#from API.app import app as api

#HOST = ''
HOST = "0.0.0.0"

PORT = 65000 # Port to listen on
ADDRESS = (HOST, PORT)

class MasterSocket:
    """
    class that will connect the agentPi to the masterPi
    """

    def main(self):
        """
        Main method call connection method to AP
        """
        MasterSocket.runConnection()
    
    def runConnection():
        """
        establishes connection point and waits for responses
        """
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(ADDRESS)
                    s.listen()

                    print("Listening on {}...".format(ADDRESS))
                    conn, addr = s.accept()
                    with conn:
                        print("Connected to {}".format(addr))
            
                        while True:
                            data = conn.recv(4096)
                            if(data != ' ' or ''):

                                print("Received {} bytes of data decoded to: '{}'".format(
                                    len(data), data.decode()))
                                msg = data.decode()

                                infoList = msg.split(",")
                                #run the database check here that the car by carid is book to that user currently
                                #if check returns true
                                #then return an 'unlock message'

                                if(infoList[0]=="unlock"):
                                    # infoList contains: unlock,username,password,carId
                                    # get results in booking where userId = username, carId = carId, bookingStatus = 'booked'
                                    # if there exists a booking that matches requirements
                                    #   then send "true"
                                    # else
                                    #   send "false"
                                    
                                    # response = api.test_client().get('/bookingsbyusers/' + infoList[1], content_type='application/json',)
                                    # data2 = json.loads(response.get_data(as_text=True))
                                    # userId = data2["loginDetails"]["userId"]


                                    conn.sendall("true".encode())
                                
                                elif(infoList[0]=="face"):
                                    # get results in booking where userId = username, carId = carId, bookingStatus = 'booked'
                                    # if there exists a booking that matches requirements
                                    #   then send "true"
                                    # else
                                    #   send "false"
                                    conn.sendall("true".encode())

                                elif(infoList[0]=="return"):
                                    # infoList contains: return,username,password
                                    # get results in booking where userId = username, carId = carId, bookingStatus = 'booked'
                                    # if there exists a booking that matches requirements
                                    #   update the booking status to finished
                                    #   then send "true"
                                    # else
                                    #   booking status not updated
                                    #   send "false"
                                    conn.sendall("true".encode())
                                
                                else:
                                    # no requirement was satisfied
                                    conn.sendall("false".encode())
                            
                                
                        #print("Sending disconnect message to agent pi")
                        #disConMsg = "disconnected, please try reconnect"
                        #conn.sendall(disConMsg.encode())

                    print("Disconnecting from client")
                print("Done.")
            except socket.error as e:
                print(("socket error {}, reconnecting").format(e))
        
    
    
if __name__ == "__main__":
    while True:
        mp = MasterSocket()
        mp.main()
