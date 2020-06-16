
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from datetime import datetime
from flaskext.mysql import MySQL
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://usergroup:Iotpi2@35.201.25.150:3306/UserDatabase'
db = SQLAlchemy(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'usergroup'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Iotpi2'
app.config['MYSQL_DATABASE_DB'] = 'UserDatabase'
app.config['MYSQL_DATABASE_HOST'] = '35.201.25.150'

mysql.init_app(app)

class Login(db.Model):
    """
    Login class, sets up the variables for the Login details table \

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
    User class, sets up the variables for the User details table \

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
    Car class, sets up the variables for the Car details table \

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

class Booking(db.Model):
    """
    Booking class, sets up the variables for the Booking details table \

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
    mechanicalIssue = db.Column(db.Text)
    ticketStatus = db.Column(db.Text)
    locationName = db.Column(db.Text)


    
    def __init__(self, bookingId, carId, userId, bookStatus, startTime, endTime, returnTime, bookingFee, customerNotes, adminNotes, mechanicalIssue, ticketStatus, locationName):
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
        self.mechanicalIssue = mechanicalIssue
        self.ticketStatus = ticketStatus
        self.locationName = locationName

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class LoginSchema(ModelSchema):
    """
    The ~Schema(ModelSchema) classes are the 'interpretation' classes between the database and the API. \
    This is the API's self contained model of the database so API calls are handled correctly before \
    database requests are sent. \
     \
    Starting with the Login table \

    """
    class Meta(ModelSchema.Meta):
        model = Login
        sqla_session = db.session
    userId = fields.String(required=True)
    passHash = fields.String(required=True)

class CarSchema(ModelSchema):
    """
    'Interpretation' class for the Car table \

    """
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
    """
    'Interpretation' class for the User table \

    """
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
    """
    'Interpretation' class for the booking table \

    """
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
    mechanicalIssue = fields.String(required=False, allow_none=True)
    ticketStatus = fields.String(required=False, allow_none=True)
    locationName = fields.String(required=False, allow_none=True)

class CreateBookingSchema(ModelSchema):
    """
    'Interpretation' class for the booking table, but for creating bookings. \
    Due to many variables not being filled when making a new booking, a new class is required \

    """
    class Meta(ModelSchema.Meta):
        model = Booking
        sqla_session = db.session
    bookingId = fields.Number(required=True)
    carId = fields.Number(required=True)
    userId = fields.String(required=True)
    bookStatus = fields.String(required=True)
    startTime = fields.DateTime(required=True)
    endTime = fields.DateTime(required=True)

@app.route('/logins/<userId>', methods = ['GET'])
def get_login_by_userid(userId):
    """
    This function returns the hashed password from the database from the entered userID \
        \
    Args: \
        userId (str): The userId to be entered \
            \
    Returns: \
        JSON response (JSON): The userId and passHash in JSON format \

    """
    get_login_by_userid = Login.query.get(userId)
    login_schema = LoginSchema(many=False)
    login_details = login_schema.dump(get_login_by_userid)
    return make_response(jsonify({"loginDetails": login_details}))    

@app.route('/logins', methods = ['GET'])
def get_all_logins():
    """
    This function returns all login details from the table, takes no arguments \

    Returns: \
        JSON response (JSON): The login table \

    """

    get_logins = Login.query.all()
    login_schema = LoginSchema(many=True)
    login_details = login_schema.dump(get_logins)
    return make_response(jsonify({"loginDetails": login_details}))

@app.route('/users/<userId>', methods = ['GET'])
def get_user_by_userid(userId):
    """
    This function returns the user details from the database from the entered userID \
    \
    Args: \
        userId (str): The userId to be entered \
            \
    Returns: \
        JSON response (JSON): User details in JSON format\

    """

    get_user_by_userid = User.query.get(userId)
    user_schema = UserSchema(many=False)
    user_details = user_schema.dump(get_user_by_userid)
    return make_response(jsonify({"userDetails": user_details}))    

@app.route('/users', methods = ['GET'])
def get_all_users():
    """
    This function returns all user details from the database, takes no arguments \
    \
    Returns: \
        JSON response (JSON): User details in JSON format \

    """

    get_users = User.query.all()
    user_schema = UserSchema(many=True)
    user_details = user_schema.dump(get_users)
    return make_response(jsonify({"userDetails": user_details}))


@app.route('/usersbyfirstname/<firstName>', methods = ['GET'])
def users_by_firstname(firstName):
    """
    This function returns the user details from the database based on firstName \
    \
    Args: \
        firstName (str): The firstName to be entered \
    \
    Returns: \
        JSON response (JSON): User details \

    """
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM UserDetails where firstName = '" + firstName + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)

    return jsonify({'usersbyfirstname' : r})
    

@app.route('/usersbylastname/<lastName>', methods = ['GET'])
def users_by_lastname(lastName):
    """
    This function returns the user details from the database based on lastName \
    \
    Args: \
        lastName (str): The lastName to be entered \
    \
    Returns: \
        JSON response (JSON): User details \

    """
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM UserDetails where lastName = '" + lastName + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)

    return jsonify({'usersbylastname' : r})
    

@app.route('/usersbyemailid/<emailId>', methods = ['GET'])
def users_by_emailId(emailId):
    """
    This function returns the user details from the database based on emailId \
    \
    Args: \
        emailId (str): The emailId to be entered \
    \
    Returns: \
        JSON response (JSON): User details \

    """
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM UserDetails where emailID = '" + emailId + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)

    return jsonify({'usersbyemailId' : r})
    

@app.route('/usersbyaccounttype/<accountType>', methods = ['GET'])
def users_by_accounttype(accountType):
    """
    This function returns the user details from the database based on accountType \
    \
    Args: \
        accountType (str): The accountType to be entered \
    \
    Returns: \
        JSON response (JSON): User details \

    """
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM UserDetails where accountType = '" + accountType + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)

    return jsonify({'usersbyaccountType' : r})
    

@app.route('/usersbyaccountstatus/<accountStatus>', methods = ['GET'])
def users_by_accountstatus(accountStatus):
    """
    This function returns the user details from the database based on accountStatus \
    \
    Args: \
        accountStatus (str): The accountStatus to be entered \
    \
    Returns: \
        JSON response (JSON): User details \

    """
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM UserDetails where accountStatus = '" + accountStatus + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)

    return jsonify({'usersbyaccountStatus' : r})
    
@app.route('/graphonepiechart', methods = ['GET'])
def graphonepiechart():
    """
    This function returns the amount of bookings of vehicles per user.  Takes no arguments \
    \
    Returns: \
        JSON response (JSON): User details \

    """
    cur = mysql.connect().cursor()
    cur.execute("select userId, count(*) as count from BookingDetails where bookStatus = 'booked' or bookStatus = 'returned' or bookStatus = 'cancelled' GROUP BY userId;;")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)

    #return jsonify(r)
    return jsonify({'graphonepiechart' : r})

    


@app.route('/bookingsbyusers/<userId>', methods = ['GET'])
def get_bookings_by_userId(userId):
    """
    This function returns the booking history from the database from the entered userID \
        \
    Args: \
        userId (str): The userId to be entered \
            \
    Returns: \
        JSON response (JSON): Booking details in JSON format \
        
    """

    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM BookingDetails where userId = '" + userId + "' ORDER BY startTime DESC;")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'bookingsbyusers' : r})


@app.route('/makenewbookingid', methods = ['GET'])
def max_bookingid():
    """
    This function returns the max bookingId from the database, takes no arguments \
    \
    Returns: \
        JSON response (JSON): Max bookingId \
    
    """

    cur = mysql.connect().cursor()
    cur.execute("SELECT MAX(bookingId) FROM BookingDetails;")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'makenewbookingid' : r})


@app.route('/makenewcarid', methods = ['GET'])
def max_carid():
    """
    This function returns the max carId from the database, takes no arguments \
    \
    Returns: \
        JSON response (JSON): Max bookingId \
    
    """

    cur = mysql.connect().cursor()
    cur.execute("SELECT MAX(carId) FROM CarDetails;")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'makenewcarid' : r})



@app.route('/carsbymakebrand/<makeBrand>', methods = ['GET'])
def cars_by_makebrand(makeBrand):
    """
    This function returns the car details from the database based on makeBrand \
    \
    Args: \
        makeBrand (str): The makeBrand to be entered \
    \
    Returns: \
        JSON response (JSON): Car details \
    
    """

    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where makeBrand = '" + makeBrand + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'carsbymakebrand' : r})


@app.route('/carsbybodytype/<bodyType>', methods = ['GET'])
def cars_by_bodyType(bodyType):
    """
    This function returns the car details from the database based on bodyType \
    \
    Args: \
        bodyType (str): The bodyType to be entered \
    \
    Returns: \
        JSON response (JSON): Car details \

    """
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where bodyType = '" + bodyType + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)

    return jsonify({'carsbybodyType' : r})
    

@app.route('/carsbycolortype/<colorType>', methods = ['GET'])
def cars_by_colorType(colorType):
    """
    This function returns the car details from the database based on colorType \
    \
    Args: \
        colorType (str): The colorType to be entered \
            \
    Returns: \
        JSON response (JSON): Car details \

    """

    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where colorType = '" + colorType + "';")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'carsbybodycolorType' : r})
    

@app.route('/carsbynumseats/<numSeats>', methods = ['GET'])
def cars_by_numSeats(numSeats):
    """
    This function returns the car details from the database based on numSeats \
        \
    Args: \
        numSeats (int): The number of seats \
            \
    Returns: \
        JSON response (JSON): Car details \

    """
    
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM CarDetails where numSeats = " + numSeats + ";")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'carsbynumSeats' : r})


@app.route('/availablecars', methods = ['GET'])
def get_available_cars():
    """
    This function returns cars from the database which either don't appear in the bookingDetails table \
    or are not currently booked in the bookingDetails table.  Takes no arguments \
        \
    Returns: \
        JSON response (JSON): carId's \
            
    """

    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM BookingDetails WHERE carId NOT IN (SELECT carId FROM BookingDetails WHERE bookStatus = 'booked' or bookStatus = 'mechanical');")
    returnNone = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.execute("SELECT carId, bodyType, makeBrand, colorType, numSeats, hourlyCost, rego FROM CarDetails LEFT JOIN BookingDetails USING (carId) WHERE BookingDetails.carId IS NULL;")
    returnBooked = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'avilablecars' : returnNone + returnBooked})


@app.route('/bookinghistorybycar/<carId>', methods = ['GET'])
def booking_history_car(carId):
    """
    This function returns the booking details by carId \
        \
    Args: \
        carId (int): Car Id \
            \
    Returns: \
        JSON response (JSON): Booking details \

    """
    
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM BookingDetails where carId = " + carId + "' ORDER BY startTime DESC;")
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'bookingDetails' : r})


@app.route('/bookings/<bookingId>', methods = ['GET'])
def get_booking_by_bookingid(bookingId):
    """
    This function returns the booking details from the database based on bookingId \
        \
    Args: \
        bookingId (int): The bookingId to search by \
            \
    Returns: \
        JSON response (JSON): Booking details \

    """

    get_booking_by_bookingid = Booking.query.get(bookingId)
    booking_schema = BookingSchema(many=False)
    booking_details = booking_schema.dump(get_booking_by_bookingid)
    return make_response(jsonify({"bookingDetails": booking_details}))    


@app.route('/bookings', methods = ['GET'])
def get_all_bookings():
    """
    This function returns all booking details, does not take arguments \
        \
    Returns: \
        JSON response (JSON): Booking details \

    """

    get_bookings = Booking.query.all()
    booking_schema = BookingSchema(many=True)
    booking_details = booking_schema.dump(get_bookings)
    return make_response(jsonify({"bookingDetails": booking_details}))

@app.route('/cars', methods = ['GET'])
def get_all_cars():
    """
    This function returns all car details, takes no arguments \
        \
    Returns: \
        JSON response (JSON): Car details \

    """

    get_cars = Car.query.all()
    cars_schema = CarSchema(many=True)
    cars_details = cars_schema.dump(get_cars)
    return make_response(jsonify({"carDetails": cars_details}))

@app.route('/cars/<carId>', methods = ['GET'])
def get_car_by_carid(carId):
    """
    This function returns the car details from the database based on carId \
        \
    Args: \
        carId (int): The carId to be entered \
            \
    Returns: \
        JSON response (JSON): Car details \

    """

    get_car_by_carid = Car.query.get(carId)
    car_schema = CarSchema(many=False)
    car_details = car_schema.dump(get_car_by_carid)
    return make_response(jsonify({"carDetails": car_details})) 


@app.route('/cars/<carId>', methods = ['DELETE'])
def delete_car_by_id(carId):
    """
    This function deletes the car from the database based on carId \
        \
    Args: \
        carId (int): The colorType to be entered \

    """

    get_car_by_carid = Car.query.get(carId)
    db.session.delete(get_car_by_carid)
    db.session.commit()
    return make_response("",204)


@app.route('/bookings/<bookingId>', methods = ['DELETE'])
def delete_booking_by_id(bookingId):
    """
    This function deletes the booking from the database based on bookingId \
        \
    Args: \
        bookingId (int): The bookingId to be entered \

    """

    get_booking_by_bookingid = Booking.query.get(bookingId)
    db.session.delete(get_booking_by_bookingid)
    db.session.commit()
    return make_response("",204)


@app.route('/users/<userId>', methods = ['DELETE'])
def delete_user_by_id(userId):
    """
    This function deletes the user from the database based on userId \
        \
    Args: \
        userId (str): The userId to be entered \

    """

    get_user_by_userid = User.query.get(userId)
    db.session.delete(get_user_by_userid)
    db.session.commit()
    return make_response("",204)


@app.route('/logins/<userId>', methods = ['DELETE'])
def delete_login_by_id(userId):
    """
    This function deletes the login information from the database based on userId \
        \
    Args: \
        userId (userId): The userId to be entered \

    """

    get_login_by_userid = Login.query.get(userId)
    db.session.delete(get_login_by_userid)
    db.session.commit()
    return make_response("",204)





@app.route('/logins', methods = ['POST'])
def create_login():
    """
    This function adds new login information into the database \
        \
    Args: \
        userId (int): The colorType to be entered \
        passHash (str): The passHash to be entered \
            
    """

    data = request.get_json()
    login_schema = LoginSchema()
    login = login_schema.load(data)
    result = login_schema.dump(login.create())
    return make_response(jsonify({"login": result}),200)

@app.route('/users', methods = ['POST'])
def create_user():
    """
    This function adds new user information into the database \
        \
    Args: \
        userId (str): The userId to be entered \
        firstName (str): The firstName to be entered \
        lastName (str): The lastName to be entered \
        emailId (str): The emailId to be entered \
        accountType (str): The accountType to be entered \
        accountStatus (str): The accountStatus to be entered \

    """

    data = request.get_json()
    user_schema = UserSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    return make_response(jsonify({"user": result}),200)

@app.route('/cars', methods = ['POST'])
def create_car():
    """
    This function adds new user information into the database \
        \
    Args: \
        carId (int): The carId to be entered \
        makeBrand  (str): The makeBrand to be entered \
        bodyType (str): The bodyType to be entered \
        rego (str): The rego to be entered \
        colorType (str): The colorType to be entered \
        numSeats (str): The numSeats to be entered \
        hourlyCost (str): The hourlyCost to be entered \
        lockStatus (bool): The lockStatus of the car \
        mechanicalIssue (str): Any mechanical issues with the car, can enter null value \
        ticketStatus (str): The ticket status of the mechanical issue, can enter null value \

    """
    data = request.get_json()
    car_schema = CarSchema()
    car = car_schema.load(data)
    result = car_schema.dump(car.create())
    return make_response(jsonify({"car": result}),200)

@app.route('/bookings', methods = ['POST'])
def create_booking():
    """
    This function adds new user information into the database \
        \
    Args: \
        bookingId (int): The bookingId to be entered \
        carId (int): The carId to be entered \
        userId (str): The userId to be entered \
        bookStatus (str): The bookStatus to be entered \
        startTime (str): The startTime to be entered \
        endTime (str): The endTime to be entered \

    """

    data = request.get_json()
    booking_schema = BookingSchema()
    booking = booking_schema.load(data)
    result = booking_schema.dump(booking.create())
    return make_response(jsonify({"booking": result}),200)


@app.route('/users/<userId>', methods = ['PUT'])
def update_user_by_userid(userId):
    """
    This function is for changing a value in the user database.  It takes three arguments, which \
    user to change (based on userId), which value to change and the value to change it to \

    """


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

@app.route('/bookings/<bookingId>', methods = ['PUT'])
def update_booking_by_bookingId(bookingId):
    """
    This function is for changing a value in the booking database.  It takes three arguments, which \
    booking to change (based on bookingId), which value to change and the value to change it to \

    """

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
    if data.get('mechanicalIssue'):
        get_booking.mechanicalIssue= data['mechanicalIssue']
    if data.get('ticketStatus'):
        get_booking.ticketStatus= data['ticketStatus']         
    if data.get('locationName'):
        get_booking.locationName= data['locationName']         
    db.session.add(get_booking)
    db.session.commit()
    booking_schema = BookingSchema(only=['bookingId', 'carId', 'userId', 'bookStatus', 'startTime', 'endTime', 'returnTime', 'bookingFee', 'customerNotes', 'adminNotes', 'mechanicalIssue', 'ticketStatus', 'locationName'])
    booking = booking_schema.dump(get_booking)
    return make_response(jsonify({"booking": booking}))

@app.route('/cars/<carId>', methods = ['PUT'])
def update_car_by_carid(carId):
    """
    This function is for changing a value in the car database.  It takes three arguments, which \
    car to change (based on carId), which value to change and the value to change it to \

    """
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


