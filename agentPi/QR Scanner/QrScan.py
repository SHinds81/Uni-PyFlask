from pyzbar import pyzbar
import datetime
import time
import cv2

class QrScan:
    """
    This class uses opencv to look at a QR image and return its data to the user
    """
    def main(self):
        """
        main method calls the scan method
        """
        QrScan.scan()


    def scan():
        """
        Scan method takes a .png file and decodes the data
        """
        img = cv2.imread('Codes/frame.png')

        codes = pyzbar.decode(img)
        
        for code in codes:
            (x, y, w, h) = code.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
            codeData = code.data.decode("utf-8")
            codeType = code.type
            
            text = "{} ({})".format(codeData, codeType)
            print (text)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            print("[INFO] Found {} Code: {}".format(codeType, codeData))

        # show the output image
        cv2.imshow("Image", img)
        cv2.waitKey(0)

if __name__ == '__main__':
    qr = QrScan()
    qr.scan()

