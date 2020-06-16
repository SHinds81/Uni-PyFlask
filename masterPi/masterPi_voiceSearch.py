import speech_recognition as sr
import subprocess
import re
import json
import sys
from API.app import app as a

class AdminUser:
    """
    This class represents the inteface where an admin can search a car by voice commands
    """
    

    def main(self):
        """
        Main method checks what the command was form the users speech then returns a json containing the information
        """
        voiceLine = AdminUser.speak()
        print('I heard: {}'.format(voiceLine))
        command = AdminUser.getCommand(voiceLine)

        print('command = {}'.format(command))
        #vaild commands, search for available/ search for user id ___/ search for car id ___
        
        try:
            if command == 'available':
                jdump = AdminUser.getCars()
                print(jdump)
            elif command == 'user':
                var = AdminUser.getVar(voiceLine, 3)
                print('searching = {}'.format(var))
                jdump = AdminUser.GetUserId(var)
                print(jdump)
            elif command == 'type':
                var = AdminUser.getVar(voiceLine, 4)
                print('searching = {}'.format(var))
                jdump = AdminUser.GetCarType(var)
                print(jdump)
            elif command == 'bookings':
                jdump = AdminUser.getBookings()
                print(jdump)
            else:
                print('could not recognize command phrase')
        except:
            print('error getting data')

            
        
        
    @a.route('/availablecars', methods = ['GET'])
    def getCars():
        """
        query the database for all available cars
        """
        
        response = a.test_client().get('/availablecars', content_type='application/json',)

        data2 = json.loads(response.get_data(as_text=True))
        return data2
        
    @a.route('/bookings', methods = ['GET'])
    def getBooikings():
        """
        query the database for all bookings
        """
        response = a.test_client().get('/bookings', content_type='application/json',)
        data2 = json.loads(response.get_data(as_text=True))
        return data2

    @a.route('/carsbybodytype/', methods = ['GET'])
    def getCarType(var): 
        """
        query the database for all cars of a cetrain body type
        """
        response = a.test_client().get('/carsbybodytype/' + var, content_type='application/json',)
        data2 = json.loads(response.get_data(as_text=True))
        return data2

    @a.route('/usersbyfirstname/', methods = ['GET'])
    def getUserName(var):
        """
        query the database for all cars of a cetrain body type
        """
        response = a.test_client().get('/usersbyfirstname/' + var, content_type='application/json',)
        data2 = json.loads(response.get_data(as_text=True))
        return data2
        
    def speak():
        """
        reads in the users speech to a string and returns that value
        """
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("say 'search for _______'")
            audio = r.listen(source)
            
            try:
                text = r.recognize_google(audio)
                print("I heard: {}".format(text))
                return text
            except:
                print("could not hear what was said")
                return ""
            
            
    
                
    def getCommand(text):
        """
        Get the key command function from the users speech
        """
        split = re.split('\s+', text)
        #print(split)
        #print(split[0])
        #print(split[1])
        try:
            if split[0] == 'search' and split[1] == 'for':
                if split[2] == 'user':
                    #search the user by first name
                    return split[2]

                elif split[2] == 'car' and split[3] == 'type':
                    #search the car by type
                    return split[3]

                else:
                    #search the command
                    return split[2]
            else:
                return "Invalid Search"
        except:
            print("search command was not recognized. Try saying 'Search for <available>'")
            
         
    def getVar(text, position):
        split = re.split('\s+', text)
        return split[position]

if __name__ == "__main__":
    au = AdminUser()
    while True:
        entry = input('Press enter to speak or x to exit')
        if entry == '':
            au.main()
        elif entry == 'x':
            sys.exit()
        else:
            'unrecognized entry, please try again'