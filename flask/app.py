"""
FRONT END API FOR CAR SHARE SYSTEM

This API handles all the data gotten from the database by the back end API and displays and
does different functions as per the requirements of this project. It now also contains 
functionality for all requirements of an admin as well.

Similiar to the back end API, it is advised that a virtual environment is used when running
this API.

The following packages must be installed prior to running this API.

pip install passlib

pip install flash

pip install request

Note: Install all other packages listed in back end API as well

To start running this API, insert the following command:
python3 -m flask run export FLASK_APP="app.py"
export FLASK_DEBUG=1
python3 -m flask run
"""

from flask import Flask, redirect, url_for, render_template, request, json, flash
from passlib.hash import sha256_crypt
from API.app import app as API
import json
import requests
import time
from googleCalendar import calendar_event as calendar

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret key'

userId = ""

class Login:
  def __init__(self, systemUserId, systemPassword, idPassed):
    self.systemUserId = request.form['username']
    self.systemPassword = request.form['password']
    self.idPassed = False
  def login(self):
    response = API.test_client().get(
        '/logins/' + self.systemUserId,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))
    userId = data2["loginDetails"]["userId"]
    passHash = data2["loginDetails"]["passHash"]

    
    if userId == self.systemUserId:
        if(sha256_crypt.verify(self.systemPassword, passHash)):
            self.idPassed = True
            return redirect(url_for('view'))
        else:
            self.idPassed = False

    return redirect(url_for('index'))


#This is the home page
@app.route("/")
def index():
    return render_template('loginPage.html')

#Handles the login process by cross checking with backend API
@app.route("/login",methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashedPassword = sha256_crypt.using(rounds = 3000).hash(password)
        response = API.test_client().get(
            '/logins/' + username, 
            content_type='application/json',
        )

        response1 = API.test_client().get(
            'users/' + username,
            content_type='application/json',
        )

        data2 = json.loads(response.get_data(as_text=True))
        data3 = json.loads(response1.get_data(as_text=True))

        userId = data2["loginDetails"]["userId"]
        passHash = data2["loginDetails"]["passHash"]
        userType = data3["userDetails"]["accountType"]

        try:
        
            if str(userType) == 'admin':
                if str(userId) == username or str(hashedPassword) == passHash:
                    if(sha256_crypt.verify(password, passHash)):
                        return render_template('adminView.html', value = username)
                flash('Invalid Login Credentials!')

            elif str(userType) != 'admin':
                if str(userId) == username or str(hashedPassword) == passHash:
                    if(sha256_crypt.verify(password, passHash)):
                        return render_template('view.html', value = username)
                flash('Invalid Login Credentials!')
            
        except:
            flash('Invalid Login Credentials!')

        return redirect(url_for('index'))

@app.route("/login", methods = ['POST'])
def returnUsername():
    # returnuser = request.form['username']
    returnuser = 'corey9'

    response = API.test_client().get(
        '/logins/' + returnuser, 
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    userId = data2["loginDetails"]["userId"]
    if str(userId) == returnuser: 
        return returnuser
    
    

#Handles signing up for new users
@app.route('/add_user', methods = ['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    usertype = request.form['usertype']
    userstatus = 'active'
    hashedPassword = sha256_crypt.using(rounds = 3000).hash(password)
    data1=json.dumps({"userId": username, "firstName": firstname, "lastName": lastname, "emailId": email, "accountType": usertype, "accountStatus": userstatus})
    data=json.dumps({"passHash": hashedPassword, "userId": username})
    
    response = API.test_client().post(
        '/logins',
        data = data,
        content_type='application/json',
    )

    response = API.test_client().post(
        '/users',
        data = data1,
        content_type='application/json',
    )

    return redirect(url_for('index'))

#Redirect for sign up page
@app.route("/createAccount/", methods = ['POST'])
def signupredirect():
    return render_template('createAccount.html')

#Redirect for login page
@app.route("/loginPage/", methods = ['POST'])
def loginredirect():
    return redirect(url_for('index'))

#Redirect for main menu
@app.route("/redirect")
def view():
    return render_template('view.html')

#Redirect for logging out and to home page
@app.route("/logout/", methods = ['POST'])
def logoutredirect():
    return redirect(url_for('index'))

#Functionality of booking history page
@app.route("/history", methods = ['POST'])
def bookinghistory():
    userid = returnUsername()
    # userid = userId

    response = API.test_client().get(
        '/bookingsbyusers/' + userid,
        content_type = 'application/json',
    )

    data = json.loads(response.get_data(as_text = True))

    return render_template('bookingHistoryResults.html', value = str(data))

#Functionality of booking history page
@app.route("/adminhistory", methods = ['POST'])
def adminbookinghistory():

    response = API.test_client().get(
        '/bookings',
        content_type = 'application/json',
    )

    data = json.loads(response.get_data(as_text = True))

    return render_template('bookingHistoryResults.html', value = str(data))

@app.route('/addremove', methods = ['POST'])
def addremove():
    return render_template('addRemoveUpdate.html')

@app.route('/removeuser', methods = ['POST'])
def removeuserredirect():
    return render_template('removeUser.html')

@app.route('/removecar', methods = ['POST'])
def removecarredirect():
    return render_template('removeCar.html')

@app.route('/removecar', methods = ['DELETE'])
def removecar():
    carid = request.form['removecriteria']
    

    response = API.test_client.delete(
        '/cars/' + carid,
        content_type = 'application/json',
    )

    flash('Car removed')
    return render_template('adminView.html')

def delete_user_information(username):
    response = API.test_client().delete(
        '/users/' + username,
        content_type='application/json',
    )


def delete_login_information(username):
    response = API.test_client().delete(
        '/logins/' + username,
        content_type='application/json',
    )

@app.route('/removeuser')
def removeuser():
    # removeinput = request.form['removecriteria']
    removeinput = "imalsoauser"

    delete_user_information(removeinput)
    delete_login_information(removeinput)

    flash('User Removed')
    return render_template('adminView.html')

    



@app.route('/addcar', methods = ['POST'])
def addcarredirect():
    return render_template('createCar.html')

def get_new_carid():
    response = API.test_client().get(
        '/makenewcarid',
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    returncarid = data["makenewcarid"][0]["MAX(carId)"]
    returncarid += 1
    return returncarid

@app.route('/createcar', methods = ['POST'])
def addcar():
    rego = request.form['rego']
    makebrand = request.form['makebrand']
    bodytype = request.form['bodytype']
    colourtype = request.form['colourtype']
    numseats = request.form['numseats']
    lockstatus = 'false'
    carId = get_new_carid()
    hourlycost = request.form['hourlycost']

    data = json.dumps({'rego':rego, 'makeBrand':makebrand, 'bodyType':bodytype, 'colorType':colourtype, 'numSeats':numseats, 'lockStatus':lockstatus, 'carId':carId, 'hourlyCost':hourlycost})

    response = API.test_client().post(
                '/cars',
                data = data,
                content_type = 'application/json',
            )
    return render_template('adminView.html')

@app.route('/adduser', methods = ['POST'])
def adduser():
    return render_template('createAccount.html')
  
#Renders all available cars
@app.route("/available", methods = ['POST'])
def availablecars():
    response = API.test_client().get(
        '/availablecars',
        content_type = 'application/json',
    )

    data = json.loads(response.get_data(as_text = True))

    return render_template('availableCars.html', value = str(data))
    
#Redirects to create new booking page
@app.route("/book", methods = ['POST'])
def createbookingredirect():
    return render_template('createBooking.html')

#Function to get next bookingid with auto increment
def get_new_bookingid():
    response = API.test_client().get(
        '/makenewbookingid',
        content_type='application/json',
    )

    data7 = json.loads(response.get_data(as_text=True))

    returnBookingId = data7["makenewbookingid"][0]["MAX(bookingId)"]
    returnBookingId += 1
    return returnBookingId



#Functionality for creating a new booking
@app.route('/createbooking', methods = ['POST'])
def createbooking():
    defineNull = None
    userId = returnUsername()
    startdate = request.form['starttime']
    enddate = request.form['endtime']
    carid = request.form['carid']
    bookstatus = 'booked'
    bookingId = get_new_bookingid()
    data=json.dumps({"userId": userId, "bookingId": bookingId, "carId": carid, "bookStatus": bookstatus, "startTime": startdate, "endTime": enddate, "returnTime": defineNull, "bookingFee": defineNull, "customerNotes": defineNull, "adminNotes": defineNull, "locationName": defineNull})

    response = API.test_client().get(
        '/cars/' + carid,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    try:
        carID = data2["carDetails"]["carId"]
        brand = data2["carDetails"]["makeBrand"]
        bodyType = data2["carDetails"]["bodyType"]
        color = data2["carDetails"]["colorType"]
        numSeats = data2["carDetails"]["numSeats"]
        hrCost = data2["carDetails"]["hourlyCost"]

        if str(carID) == carid:
            response1 = API.test_client().post(
                '/bookings',
                data = data,
                content_type = 'application/json',
            )
            #Creates new calendar event
            cal = calendar.GoogleCalendar()
            cal.creatEvent(defineNull, "location", carID, brand, bodyType, color, numSeats, hrCost, startdate, enddate)
            return render_template('view.html')
            
    except:
        flash('Invalid CarID')
    
    return render_template('view.html')
        
    
#Redirect to search car page
@app.route('/search', methods = ['POST'])
def searchforcar():
    return render_template('searchCar.html')

#Redirect to search car page
@app.route('/searchuser', methods = ['POST'])
def searchforuser():
    return render_template('searchUser.html')

#Search car details by carid
@app.route('/carid', methods = ['POST'])
def searchbycarid():
    search = request.form['searchcriteria']
    response = API.test_client().get(
        '/cars/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = str(data2))
    
#Search car details by bodytype
@app.route('/bodytype', methods = ['POST'])
def searchbybodytype():
    search = request.form['searchcriteria']

    response = API.test_client().get(
        '/carsbybodytype/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

#Search car details by makebrand
@app.route('/makebrand', methods = ['POST'])
def searchbymakebrand():
    search = request.form['searchcriteria']

    response = API.test_client().get(
        '/carsbymakebrand/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

#Search car details by colour
@app.route('/colourtype', methods = ['POST'])
def searchbycolourtype():
    search = request.form['searchcriteria']

    response = API.test_client().get(
        '/carsbybodytype/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

#Search car details by number of seats
@app.route('/numseats', methods = ['POST'])
def searchbynumseats():
    search = request.form['searchcriteria']

    response = API.test_client().get(
        '/carsbynumseats/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

@app.route('/userid', methods = ['POST'])
def searchbyuserid():
    search = request.form['searchuser']

    response = API.test_client().get(
        '/users/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

@app.route('/firstname', methods = ['POST'])
def searchbyfirstname():
    search = request.form['searchuser']

    response = API.test_client().get(
        '/usersbyfirstname/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

@app.route('/lastname', methods = ['POST'])
def searchbylastname():
    search = request.form['searchuser']

    response = API.test_client().get(
        '/usersbylastname/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

@app.route('/email', methods = ['POST'])
def searchbyemail():
    search = request.form['searchuser']

    response = API.test_client().get(
        '/usersbyemailid/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

@app.route('/accounttype', methods = ['POST'])
def searchbyaccounttype():
    search = request.form['searchuser']

    response = API.test_client().get(
        '/usersbyaccounttype/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

@app.route('/accountstatus', methods = ['POST'])
def searchbyaccountstatus():
    search = request.form['searchuser']

    response = API.test_client().get(
        '/usersbyaccountstatus/' + search,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('results.html', value = data2)

#Gets username of current user to display all bookings to cancel
@app.route('/cancel', methods = ['POST'])
def cancelbooking():
    test= returnUsername()

    response = API.test_client().get(
        '/bookingsbyusers/' + test,
        content_type = 'application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    return render_template('cancelBookingResults.html', value = data2)

#Functionality for cancelling booking
@app.route('/cancelbookingfinal', methods = ['PUT'])
def cancelbookingfinal():
    bookingID = request.form['bookingid']
    newBookStatus = 'Cancelled'

    response = API.test_client().put(
        '/bookings/' + bookingID,
        data=json.dumps({"bookStatus": newBookStatus}),
        content_type='application/json',
    )
    
    flash('Booking has been cancelled')

    return redirect(url_for('view'))

@app.route('/updateuser', methods = ['POST'])
def updateuserredirect():
    return render_template('updateUser.html')

@app.route('/updatecar', methods = ['POST'])
def updatecarredirect():
    return render_template('updateCar.html')

def firstnameupdate(userid, firstname):
    response = API.test_client().put(
       '/users/' + userid,
        data=json.dumps({"firstName": firstname}),
        content_type='application/json',
    )

def lastnameupdate(userid, lastname):
    response = API.test_client().put(
       '/users/' + userid,
        data=json.dumps({"lastName": lastname}),
        content_type='application/json',
    )

def emailupdate(userid, email):
    response = API.test_client().put(
       '/users/' + userid,
        data=json.dumps({"emailId": email}),
        content_type='application/json',
    )

def accounttypeupdate(userid, accounttype):
    response = API.test_client().put(
       '/users/' + userid,
        data=json.dumps({"accountType": accounttype}),
        content_type='application/json',
    )

def accountstatusupdate(userid, accountstatus):
    response = API.test_client().put(
       '/users/' + userid,
        data=json.dumps({"accountStatus": accountstatus}),
        content_type='application/json',
    )

def regoupdate(carid, rego):
    response = API.test_client().put(
       '/cars/' + carid,
        data=json.dumps({"rego": rego}),
        content_type='application/json',
    )

def bodytypeupdate(carid, bodytype):
    response = API.test_client().put(
       '/cars/' + carid,
        data=json.dumps({"bodyType": bodytype}),
        content_type='application/json',
    )

def makebrandupdate(carid, makebrand):
    response = API.test_client().put(
       '/cars/' + carid,
        data=json.dumps({"makeBrand": makebrand}),
        content_type='application/json',
    )

def colourtypeupdate(carid, colourtype):
    response = API.test_client().put(
       '/cars/' + carid,
        data=json.dumps({"colorType": colourtype}),
        content_type='application/json',
    )

def numseatsupdate(carid, numseats):
    response = API.test_client().put(
       '/cars/' + carid,
        data=json.dumps({"numSeats": numseats}),
        content_type='application/json',
    )

def hourlycostupdate(carid, hourlycost):
    response = API.test_client().put(
       '/cars/' + carid,
        data=json.dumps({"hourlyCost": hourlycost}),
        content_type='application/json',
    )

@app.route('/updaterego', methods = ['POST'])
def updateregoredirect():
    return render_template('updateRego.html')

@app.route('/updatemakebrand', methods = ['POST'])
def updatemakebrandredirect():
    return render_template('updateMakeBrand.html')

@app.route('/updatebodytype', methods = ['POST'])
def updatebodytyperedirect():
    return render_template('updateBodyType.html')

@app.route('/updatecolourtype', methods = ['POST'])
def updatecolourtyperedirect():
    return render_template('updateColourType.html')

@app.route('/updatenumseats', methods = ['POST'])
def updatenumseatsredirect():
    return render_template('updateNumSeats.html')

@app.route('/updatehourlycost', methods = ['POST'])
def updatehourlycostredirect():
    return render_template('updateHourlyCost.html')

@app.route('/updatefirstname', methods = ['POST'])
def updatefirstnameredirect():
    return render_template('updateFirstName.html')

@app.route('/updatelastname', methods = ['POST'])
def updatelastnameredirect():
    return render_template('updateLastName.html')

@app.route('/updateemail', methods = ['POST'])
def updateEmailredirect():
    return render_template('updateEmail.html')

@app.route('/updateaccounttype', methods = ['POST'])
def updateaccounttyperedirect():
    return render_template('updateAccountType.html')

@app.route('/updateaccountstatus', methods = ['POST'])
def updateaccountstatusredirect():
    return render_template('updateAccountStatus.html')

@app.route('/changerego')
def updaterego():
    carid = request.form['carid']
    rego = request.form['regochange']

    regoupdate(carid, rego)

    return render_template('updateCar.html')

@app.route('/changerego')
def updatebodytype():
    carid = request.form['carid']
    bodytype = request.form['bodytypechange']

    bodytypeupdate(carid, rego)

    return render_template('updateCar.html')

@app.route('/changemakebrand')
def updatemakebrand():
    carid = request.form['carid']
    makebrand = request.form['makebrandchange']

    makebrandupdate(carid, makebrand)

    return render_template('updateCar.html')

@app.route('/changecolourtype')
def updatecolourtype():
    carid = request.form['carid']
    colourtype = request.form['colourtypechange']

    colourtypeupdate(carid, colourtype)

    return render_template('updateCar.html')

@app.route('/changerego')
def updatenumseats():
    carid = request.form['carid']
    numseats = request.form['numseatschange']

    numseatsupdate(carid, numseats)

    return render_template('updateCar.html')

@app.route('/changerego')
def updatehourlycost():
    carid = request.form['carid']
    hourlycost = request.form['hourlycostchange']

    regoupdate(carid, hourlycost)

    return render_template('updateCar.html')

@app.route('/changefirstname')
def updatefirstname():
    userid = request.form['userid']
    firstname = request.form['firstnamechange']

    firstnameupdate(userid, firstname)

    return render_template('adminView.html')

@app.route('/changelastname')
def updatelastname():
    userid = request.form['userid']
    lastname = request.form['lastnamechange']

    firstnameupdate(userid, lastname)

    return render_template('adminView.html')

@app.route('/changeemail')
def updateemail():
    userid = request.form['userid']
    email = request.form['emailchange']

    emailupdate(userid, email)

    return render_template('adminView.html')

@app.route('/changeaccountstatus')
def updateaccountstatus():
    userid = request.form['userid']
    accountstatus = request.form['accountstatusselect']

    accountstatusupdate(userid, accountstatus)

    return render_template('adminView.html')

@app.route('/changeaccounttype')
def updateaccounttype():
    userid = request.form['userid']
    usertype = request.form['usertype']

    accounttypeupdate(userid, usertype)

    return render_template('adminView.html')

def update_booking_for_tech(newBookingId, newBookStatus, newMechanicalIssue, newTicketStatus):
    response = API.test_client().put(
       '/bookings/' + newBookingId,
        data=json.dumps({"bookStatus": newBookStatus}),
        content_type='application/json',
    )

    #data2 = json.loads(response.get_data(as_text=True))

    response = API.test_client().put(
       '/bookings/' + newBookingId,
        data=json.dumps({"mechanicalIssue": newMechanicalIssue}),
        content_type='application/json',
    )

    #data2 = json.loads(response.get_data(as_text=True))

    response = API.test_client().put(
       '/bookings/' + newBookingId,
        data=json.dumps({"ticketStatus": newTicketStatus}),
        content_type='application/json',
    )

    #data2 = json.loads(response.get_data(as_text=True))

@app.route('/reportcar', methods = ['POST'])
def reportcarredirect():
    return render_template('reportCar.html')

@app.route('/reportissue')
def reportcar():
    bookingid = request.form['reportbookingid']
    # bookingid = '1006.0'
    issue = request.form['carissue']
    # issue = 'Engine Problem'
    ticketstatus = "toBeFixed"
    newBookStatus = "Mechanical"

    update_booking_for_tech(bookingid, newBookStatus, issue, newBookStatus)

    # flash("Car reported")

    return render_template('adminView.html')



#Main function to run flask program
if __name__ == '__main__':
    app.run(debug=True)




