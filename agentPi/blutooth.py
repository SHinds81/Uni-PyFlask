import bluetooth
import os
import time
#from sense_hat import SenseHat

def main():
    """
    Main method that calls the bluetooth search function
    """
    #user_name = input("Enter your name: ")
    #device_address = None
    #device_name = input("Enter engineers device name: ")
    search()
    
    
def search():
    """
    Method that first searches for know engineer devices and returns true if found.
    else gets the name of an egineers bluetooth device and searches if it exist. if it does return true, else return false
    """
    device_address = None
    myMac = '80:ED:2C:A7:6B:3A'
    
    nearby_devices = bluetooth.discover_devices()
    for mac_address in nearby_devices:
        if mac_address == myMac:
            return True
    
    device_name = input("Enter engineers device name: ")
        
    dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
    print("\nCurrently: {}".format(dt))
    time.sleep(3) #Sleep three seconds 
    nearby_devices = bluetooth.discover_devices()
    for mac_address in nearby_devices:
        if device_name == bluetooth.lookup_name(mac_address, timeout=5):
            device_address = mac_address
            print('break')
            break
        
    if device_address is not None:
        print(device_address)
        print(mac_address)
        #print("Hello Engineer! Car is unlocked".format(device_name))
        #sense = SenseHat()
        #Unlock the car
        return True
    else:
        print('false')
        #print("Could not identify device. Try again")
        return False

#Execute program
if __name__ == "__main__":
    main()
