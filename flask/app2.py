from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from datetime import datetime
from flaskext.mysql import MySQL
#from db_config import mysql
#from mysql import MySQL
#import pymysql


"""
Back end API for Car Share System

It is recommended that the API should sit in it's own directory, then consumed by
front end system.

For example, if the API is in the "API" subdirectory of the front end system, it 
should be imported like this:

from API.app import app as API


Then, when accessing the API, methods should be called like this:

def get_all_car_information():
    response = API.test_client().get(
        '/cars',
        content_type='application/json',
    )

The empty file "__init__.py" has to be in the same directory as the API for the API
to be consumed properly.

To run the API, make sure the following steps are taken:
Make a virtual environment and activate:
python3 -m venv <myenvname>
source <myenvname>/bin/activate

The following packages need to be installed into the virtual environment:
pip install flask flask-sqlalchemy

pip install marshmallow-sqlalchemy

pip install pymysql

pip install requests

Note: These packages have to be installed on the front end system as well


The API then needs to start running.  Flask default is port 5000, so a different port is required
if the front end is a flask application running on the default port.  This command runs the API at
port 5001 to resolve the conflict:
flask run --host 0.0.0.0 --port 5001
"""


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://usergroup:Iotpi2@35.201.25.150:3306/UserDatabase'
db = SQLAlchemy(app)
"""
This sets up the connection string and base starting parameters for the database
"""


mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'usergroup'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Iotpi2'
app.config['MYSQL_DATABASE_DB'] = 'UserDatabase'
#app.config['MYSQL_DATABASE_HOST'] = '35.201.25.150:3306'
app.config['MYSQL_DATABASE_HOST'] = '35.201.25.150'

mysql.init_app(app)


class Login(db.Model):
    """
    Login class, sets up the variables for the Login details table
    """
    __tablename__ = "LoginDetails"
    userId = db.Column(db.Text, primary_key=True)
    passHash = db.Column(db.Text)

    def __init__(self, userId, passHash):
        self.userId = userId
        self.passHash = passHash

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class User(db.Model):
    """
    User class, sets up the variables for the User details table
    """
    __tablename__ = "UserDetails"
    userId = db.Column(db.Text, primary_key=True)
    firstName = db.Column(db.Text)
    lastName = db.Column(db.Text)
    emailId = db.Column(db.Text)
    accountType = db.Column(db.Text)
    accountStatus = db.Column(db.Text)

    def __init__(self, userId, firstName, lastName, emailId, accountType, accountStatus):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.emailId = emailId
        self.accountType = accountType
        self.accountStatus = accountStatus

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Car(db.Model):
    """
    Car class, sets up the variables for the Car details table
    """
    __tablename__ = "CarDetails"
    carId = db.Column(db.Integer, primary_key=True)
    makeBrand = db.Column(db.Text)
    bodyType = db.Column(db.Text)
    rego = db.Column(db.Text)
    colorType = db.Column(db.Text)
    numSeats = db.Column(db.Integer)
    hourlyCost = db.Column(db.Float)
    lockStatus = db.Column(db.Boolean)

    def __init__(self, carId, makeBrand, bodyType, rego, colorType, numSeats, hourlyCost, lockStatus):
        self.carId = carId
        self.makeBrand = makeBrand
        self.bodyType = bodyType
        self.rego = rego
        self.colorType = colorType
        self.numSeats = numSeats
        self.hourlyCost = hourlyCost
        self.lockStatus = lockStatus

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


    """
class CreateBooking(db.Model):
    __tablename__ = "BookingDetails"
    bookingId = db.Column(db.Integer, primary_key=True)
    carId = db.Column(db.Integer)
    userId = db.Column(db.Text)
    bookStatus = db.Column(db.Text)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)

    
    
    def __init__(self, bookingId, carId, userId, bookStatus, startTime, endTime):
        self.bookingId = bookingId
        self.carId = carId
        self.userId = userId
        self.bookStatus = bookStatus
        self.startTime = startTime
        self.endTime = endTime
    """



class Booking(db.Model):
    """
    Booking class, sets up the variables for the Booking details table
    """
    __tablename__ = "BookingDetails"
    bookingId = db.Column(db.Integer, primary_key=True)
    carId = db.Column(db.Integer)
    userId = db.Column(db.Text)
    bookStatus = db.Column(db.Text)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    returnTime = db.Column(db.DateTime)
    bookingFee = db.Column(db.Float)
    customerNotes = db.Column(db.Text) 
    adminNotes = db.Column(db.Text)
    locationName = db.Column(db.Text)


    
    def __init__(self, bookingId, carId, userId, bookStatus, startTime, endTime, returnTime, bookingFee, customerNotes, adminNotes, locationName):
        self.bookingId = bookingId
        self.carId = carId
        self.userId = userId
        self.bookStatus = bookStatus
        self.startTime = startTime
        self.endTime = endTime
        self.returnTime = returnTime
        self.bookingFee = bookingFee
        self.customerNotes = customerNotes
        self.adminNotes = adminNotes
        self.locationName = locationName
    

    """
    def __init__(self, bookingId, carId, userId, bookStatus, startTime, endTime):
        self.bookingId = bookingId
        self.carId = carId
        self.userId = userId
        self.bookStatus = bookStatus
        self.startTime = startTime
        self.endTime = endTime
    """

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

"""
The ~Schema(ModelSchema) classes are the 'interpretation' classes between the database and the API.
This is the API's self contained model of the database so API calls are handled correctly before
database requests are sent.
"""
class LoginSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Login
        sqla_session = db.session
    userId = fields.String(required=True)
    passHash = fields.String(required=True)

class CarSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Car
        sqla_session = db.session
    carId = fields.Number(required=True)
    makeBrand = fields.String(required=True)
    bodyType = fields.String(required=True)
    rego = fields.String(required=True)
    colorType = fields.String(required=True)
    numSeats = fields.Number(required=True)
    hourlyCost = fields.Float(required=True)
    lockStatus = db.Boolean()

class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session
    userId = fields.String(required=True)
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    emailId = fields.String(required=True)
    accountType = fields.String(required=True)
    accountStatus = fields.String(required=True)


class BookingSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Booking
        sqla_session = db.session
    bookingId = fields.Number(required=True)
    carId = fields.Number(required=True)
    userId = fields.String(required=True)
    bookStatus = fields.String(required=True)
    startTime = fields.DateTime(required=True)
    endTime = fields.DateTime(required=True)
    returnTime = fields.DateTime(required=False, allow_none=True)
    bookingFee = fields.Decimal(required=False, allow_none=True)
    customerNotes = fields.String(required=False, allow_none=True) 
    adminNotes = fields.String(required=False, allow_none=True)
    locationName = fields.String(required=False, allow_none=True)

class CreateBookingSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Booking
        sqla_session = db.session
    bookingId = fields.Number(required=True)
    carId = fields.Number(required=True)
    userId = fields.String(required=True)
    bookStatus = fields.String(required=True)
    startTime = fields.DateTime(required=True)
    endTime = fields.DateTime(required=True)


#Get login info by userID
@app.route('/logins/<userId>', methods = ['GET'])
def get_login_by_userid(userId):
    get_login_by_userid = Login.query.get(userId)
    login_schema = LoginSchema(many=False)
    login_details = login_schema.dump(get_login_by_userid)
    return make_response(jsonify({"loginDetails": login_details}))    

#get all logins
@app.route('/logins', methods = ['GET'])
def get_all_logins():
    get_logins = Login.query.all()
    login_schema = LoginSchema(many=True)
    login_details = login_schema.dump(get_logins)
    return make_response(jsonify({"loginDetails": login_details}))

#Get user info by userID
@app.route('/users/<userId>', methods = ['GET'])
def get_user_by_userid(userId):
    get_user_by_userid = User.query.get(userId)
    user_schema = UserSchema(many=False)
    user_details = user_schema.dump(get_user_by_userid)
    return make_response(jsonify({"userDetails": user_details}))    

#get all user info
@app.route('/users', methods = ['GET'])
def get_all_users():
    get_users = User.query.all()
    user_schema = UserSchema(many=True)
    user_details = user_schema.dump(get_users)
    return make_response(jsonify({"userDetails": user_details}))

"""
#Get bookings info by userID
@app.route('/bookings/users/<userId>', methods = ['GET'])
def get_booking_by_userid(userId):
    get_booking_by_userid = Booking.query.get(userId)
    booking_schema = BookingSchema(many=True)
    booking_details = booking_schema.dump(get_booking_by_userid)
    return make_response(jsonify({"bookingDetails": booking_details}))    
"""


#Get booking info by userID
@app.route('/bookingsbyusers/<userId>', methods = ['GET'])
def get_bookings_by_userId(userId):
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM BookingDetails where userId = '" + userId + "' ORDER BY startTime DESC;")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'bookingsbyusers' : r})


#Get max booking Id
@app.route('/makenewbookingid', methods = ['GET'])
def max_bookingid():
    cur = mysql.connect().cursor()
    cur.execute("SELECT MAX(bookingId) FROM BookingDetails;")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'makenewbookingid' : r})


#Get cars by makeBrand
@app.route('/carsbymakebrand/<makeBrand>', methods = ['GET'])
def cars_by_makebrand(makeBrand):
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where makeBrand = '" + makeBrand + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'carsbymakebrand' : r})


#Get cars by bodyType
@app.route('/carsbybodytype/<bodyType>', methods = ['GET'])
def cars_by_bodyType(bodyType):
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where bodyType = '" + bodyType + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'carsbybodyType' : r})
    

#Get cars by colorType
@app.route('/carsbybodytype/<colorType>', methods = ['GET'])
def cars_by_colorType(colorType):
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where colorType = '" + colorType + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'carsbybodycolorType' : r})
    

#Get cars by numSeats
@app.route('/carsbynumseats/<numSeats>', methods = ['GET'])
def cars_by_numSeats(numSeats):
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where numSeats = " + numSeats + ";")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'carsbynumSeats' : r})


#get available cars
@app.route('/availablecars', methods = ['GET'])
def get_available_cars():
    cur = mysql.connect().cursor()
    cur.execute("select carId, bodyType, makeBrand, colorType, numSeats, hourlyCost, rego from CarDetails LEFT JOIN BookingDetails USING (carId) where BookingDetails.bookStatus <> 'booked';")
    returnNone = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.execute("SELECT carId, bodyType, makeBrand, colorType, numSeats, hourlyCost, rego FROM CarDetails LEFT JOIN BookingDetails USING (carId) WHERE BookingDetails.carId IS NULL;")
    returnBooked = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'avilablecars' : returnNone + returnBooked})
    #return jsonify({'avilablecars' : returnBooked})

"""
    cur.execute("select * from BookingDetails where bookStatus <> 'booked';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'avilablecars' : r})
"""



#Get bookings info by bookingID
@app.route('/bookings/<bookingId>', methods = ['GET'])
def get_booking_by_bookingid(bookingId):
    get_booking_by_bookingid = Booking.query.get(bookingId)
    booking_schema = BookingSchema(many=False)
    booking_details = booking_schema.dump(get_booking_by_bookingid)
    return make_response(jsonify({"bookingDetails": booking_details}))    


#get all booking info
@app.route('/bookings', methods = ['GET'])
def get_all_bookings():
    get_bookings = Booking.query.all()
    booking_schema = BookingSchema(many=True)
    booking_details = booking_schema.dump(get_bookings)
    return make_response(jsonify({"bookingDetails": booking_details}))

#get all car info
@app.route('/cars', methods = ['GET'])
def get_all_cars():
    get_cars = Car.query.all()
    cars_schema = CarSchema(many=True)
    cars_details = cars_schema.dump(get_cars)
    return make_response(jsonify({"carDetails": cars_details}))

#Get car info by carID
@app.route('/cars/<carId>', methods = ['GET'])
def get_car_by_carid(carId):
    get_car_by_carid = Car.query.get(carId)
    car_schema = CarSchema(many=False)
    car_details = car_schema.dump(get_car_by_carid)
    return make_response(jsonify({"carDetails": car_details})) 




#Delete car by carID
@app.route('/cars/<carId>', methods = ['DELETE'])
def delete_car_by_id(carId):
    get_car_by_carid = Car.query.get(carId)
    db.session.delete(get_car_by_carid)
    db.session.commit()
    return make_response("",204)


#Delete booking by bookingID
@app.route('/bookings/<bookingId>', methods = ['DELETE'])
def delete_booking_by_id(bookingId):
    get_booking_by_bookingid = Booking.query.get(bookingId)
    db.session.delete(get_booking_by_bookingid)
    db.session.commit()
    return make_response("",204)

#Delete user by userID
@app.route('/users/<userId>', methods = ['DELETE'])
def delete_user_by_id(userId):
    get_user_by_userid = User.query.get(userId)
    db.session.delete(get_user_by_userid)
    db.session.commit()
    return make_response("",204)

#Delete login by userID
@app.route('/logins/<userId>', methods = ['DELETE'])
def delete_login_by_id(userId):
    get_login_by_userid = Login.query.get(userId)
    db.session.delete(get_login_by_userid)
    db.session.commit()
    return make_response("",204)





#POST METHODS (new row of data)
@app.route('/logins', methods = ['POST'])
def create_login():
    data = request.get_json()
    login_schema = LoginSchema()
    login = login_schema.load(data)
    result = login_schema.dump(login.create())
    return make_response(jsonify({"login": result}),200)

@app.route('/users', methods = ['POST'])
def create_user():
    data = request.get_json()
    user_schema = UserSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    return make_response(jsonify({"user": result}),200)

@app.route('/cars', methods = ['POST'])
def create_car():
    data = request.get_json()
    car_schema = CarSchema()
    car = car_schema.load(data)
    result = car_schema.dump(car.create())
    return make_response(jsonify({"car": result}),200)

@app.route('/bookings', methods = ['POST'])
def create_booking():
    data = request.get_json()
    booking_schema = BookingSchema()
    booking = booking_schema.load(data)
    result = booking_schema.dump(booking.create())
    return make_response(jsonify({"booking": result}),200)


#PUT methods (update row methods)
#update user by userId
@app.route('/users/<userId>', methods = ['PUT'])
def update_user_by_userid(userId):
    data = request.get_json()
    get_user = User.query.get(userId)
    if data.get('userId'):
        get_user.userId = data['userId']
    if data.get('firstName'):
        get_user.firstName = data['firstName']
    if data.get('lastName'):
        get_user.lastName = data['lastName']
    if data.get('emailId'):
        get_user.emailId= data['emailId']    
    if data.get('accountType'):
        get_user.accountType= data['accountType']    
    if data.get('accountStatus'):
        get_user.accountStatus= data['accountStatus']    
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema(only=['userId', 'firstName', 'lastName','emailId','accountType','accountStatus'])
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))

#update booking by bookingid
@app.route('/bookings/<bookingId>', methods = ['PUT'])
def update_booking_by_bookingId(bookingId):
    data = request.get_json()
    get_booking = Booking.query.get(bookingId)
    if data.get('bookingId'):
        get_booking.bookingId = data['bookingId']
    if data.get('carId'):
        get_booking.carId = data['carId']
    if data.get('userId'):
        get_booking.userId = data['userId']
    if data.get('bookStatus'):
        get_booking.bookStatus= data['bookStatus']    
    if data.get('startTime'):
        get_booking.startTime= data['startTime']    
    if data.get('endTime'):
        get_booking.endTime= data['endTime']
    if data.get('returnTime'):
        get_booking.returnTime= data['returnTime']
    if data.get('bookingFee'):
        get_booking.bookingFee= data['bookingFee']
    if data.get('customerNotes'):
        get_booking.customerNotes= data['customerNotes']
    if data.get('adminNotes'):
        get_booking.adminNotes= data['adminNotes']     
    if data.get('location'):
        get_booking.location= data['location']         
    db.session.add(get_booking)
    db.session.commit()
    booking_schema = BookingSchema(only=['bookingId', 'carId', 'userId','bookStatus','startTime','endTime','returnTime','bookingFee','customerNotes','adminNotes','location'])
    booking = booking_schema.dump(get_booking)
    return make_response(jsonify({"booking": booking}))

#update car by carId
@app.route('/cars/<carId>', methods = ['PUT'])
def update_car_by_carid(carId):
    data = request.get_json()
    get_car = Car.query.get(carId)
    if data.get('carId'):
        get_car.carId = data['carId']
    if data.get('makeBrand'):
        get_car.makeBrand = data['makeBrand']
    if data.get('bodyType'):
        get_car.bodyType = data['bodyType']
    if data.get('rego'):
        get_car.rego = data['rego']    
    if data.get('colorType'):
        get_car.colorType= data['colorType']    
    if data.get('numSeats'):
        get_car.numSeats= data['numSeats']    
    if data.get('hourlyCost'):
        get_car.hourlyCost= data['hourlyCost']    
    if data.get('lockStatus'):
        get_car.lockStatus= data['lockStatus']
    db.session.add(get_car)
    db.session.commit()
    get_car_schema = CarSchema(only=['carId', 'makeBrand', 'bodyType','rego','colorType','numSeats','hourlyCost','lockStatus'])
    car = get_car_schema.dump(get_car)
    return make_response(jsonify({"car": car}))


