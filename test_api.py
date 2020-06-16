from API.app import app as API
from flask import json
import requests
import pytest


#Testing methods
def create_login_information(username, password):
    response = API.test_client().post(
        '/logins',
        data=json.dumps({"userId": username, "passHash": password}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/logins/' + username,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnUser = data2["loginDetails"]["userId"]
    returnPass = data2["loginDetails"]["passHash"]
    return returnUser
    return returnPass


def update_login_information(username, newpassword):
    response = API.test_client().put(
       '/logins/' + username,
        data=json.dumps({"passHash": newpassword}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/logins/' + username,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnUser = data2["loginDetails"]["userId"]
    returnPass = data2["loginDetails"]["passHash"]
    return returnUser
    return returnPass


def create_user_information(username, testingFirstName, testingLastName, testingEmailID, testingAccountType, testingAccountStatus):
    response = API.test_client().post(
        '/users',
        data=json.dumps({"userId": username, "firstName": testingFirstName, "lastName": testingLastName, "emailId": testingEmailID, "accountType": testingAccountType, "accountStatus": testingAccountStatus}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/users/' + username,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnEmailID = data2["userDetails"]["emailId"]
    return returnEmailID


def update_user_information(username, newaccountstatus):
    response = API.test_client().put(
       '/users/' + username,
        data=json.dumps({"accountStatus": newaccountstatus}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/users/' + username,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnAccountStatus = data2["userDetails"]["accountStatus"]
    return returnAccountStatus


def create_car_information(testingCarId, testingMakeBrand, testingBodyType, testingRego, testingColorType, testingNumSeats, testingHourlyCost, testingLockStatus):
    response = API.test_client().post(
        '/cars',
        data=json.dumps({"carId": testingCarId, "makeBrand": testingMakeBrand, "bodyType": testingBodyType, "rego": testingRego, "colorType": testingColorType, "numSeats": testingNumSeats, "hourlyCost": testingHourlyCost, "lockStatus": testingLockStatus}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/cars/' + testingCarId,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnCarId = data2["carDetails"]["carId"]
    returnMakeBrand = data2["carDetails"]["makeBrand"]
    returnBodyType = data2["carDetails"]["bodyType"]
    returnRego = data2["carDetails"]["rego"]
    returnColorType = data2["carDetails"]["colorType"]
    returnNumSeats = data2["carDetails"]["numSeats"]
    returnHourlyCost = data2["carDetails"]["hourlyCost"]
    returnLockStatus = data2["carDetails"]["lockStatus"]

    return returnBodyType
    return returnMakeBrand
    


def update_car_information(testingCarId, testingNewLockStatus):
    response = API.test_client().put(
       '/cars/' + testingCarId,
        data=json.dumps({"colorType": testingNewLockStatus}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/cars/' + testingCarId,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnCarId = data2["carDetails"]["makeBrand"]
    returnLockStatus = data2["carDetails"]["colorType"]
    return returnLockStatus



def create_booking_information(testingBookingId, testingCarId, testingUsername, testingBookStatus, testingStartTime, testingEndTime):
    defineNull = None
    response = API.test_client().post(
        '/bookings',
        data=json.dumps({"bookingId": testingBookingId, "carId": testingCarId, "userId": testingUsername, "bookStatus": testingBookStatus, "startTime": testingStartTime, "endTime": testingEndTime, "returnTime": defineNull, "bookingFee": defineNull, "customerNotes": defineNull, "adminNotes": defineNull, "mechanicalIssue": defineNull, "ticketStatus": defineNull, "locationName": defineNull}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/bookings/' + testingBookingId,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnBookStatus = data2["bookingDetails"]["bookStatus"]
    return returnBookStatus

def update_booking_information(testingBookingId, testingAdminNote):
    response = API.test_client().put(
       '/bookings/' + testingBookingId,
        data=json.dumps({"adminNotes": testingAdminNote}),
        content_type='application/json',
    )

    response = API.test_client().get(
        '/bookings/' + testingBookingId,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnAdminNote = data2["bookingDetails"]["adminNotes"]
    return returnAdminNote

def delete_booking_information(bookingnumber):
    response = API.test_client().delete(
        '/bookings/' + bookingnumber,
        content_type='application/json',
    )


    response = API.test_client().get(
        '/bookings/' + bookingnumber,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnUser = data2["bookingDetails"]["bookingId"]
    return returnUser

def delete_car_information(carnumber):
    response = API.test_client().delete(
        '/cars/' + carnumber,
        content_type='application/json',
    )


    response = API.test_client().get(
        '/bookings/' + carnumber,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnUser = data2["carDetails"]["carId"]
    return returnUser

def delete_user_information(username):
    response = API.test_client().delete(
        '/users/' + username,
        content_type='application/json',
    )


    response = API.test_client().get(
        '/users/' + username,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnUser = data2["userDetails"]["userId"]
    return returnUser

def delete_login_information(username):
    response = API.test_client().delete(
        '/logins/' + username,
        content_type='application/json',
    )


    response = API.test_client().get(
        '/logins/' + username,
        content_type='application/json',
    )

    data2 = json.loads(response.get_data(as_text=True))

    returnUser = data2["loginDetails"]["userId"]
    return returnUser


#Variables used for testing
testingUsername = "TestUsername"
testingPassword = "TestPassword"

testingNewPassword = "TestSecondPassword"


testingFirstName = "Testlies"
testingLastName = "Testname"
testingEmailID = "test@test.net.au"
testingAccountType = "Testing"
testingAccountStatus = "suspended"

testingNewAccountStatus = "active"


testingCarId = str(555)
testingMakeBrand = "TestMake"
testingBodyType = "TestWagon"
testingRego = "TEST555"
testingColorType = "TestColor"
testingNumSeats = 5
testingHourlyCost = 5.5
testingLockStatus = False

testingNewLockStatus = "Changed Color"


testingBookingId = str(444)
testingBookStatus = "Testing"
testingStartTime = "2020-6-15 14:30:23"
testingEndTime = "2020-7-20 16:15:58"

testingAdminNote = "Testing Update Notification"

#test adding new login
def test_login_add():
    assert create_login_information(testingUsername, testingPassword) == testingUsername, testingPassword

#test updating login password
def test_login_update():
    assert update_login_information(testingUsername, testingNewPassword) == testingUsername, testingNewPassword

#test adding new user
def test_user_add():
    assert create_user_information(testingUsername, testingFirstName, testingLastName, testingEmailID, testingAccountType, testingAccountStatus) == testingEmailID

#test updating user account status 
def test_user_update():
    assert update_user_information(testingUsername, testingNewAccountStatus) == testingNewAccountStatus

#test adding new car
def test_car_add():
    assert create_car_information(testingCarId, testingMakeBrand, testingBodyType, testingRego, testingColorType, testingNumSeats, testingHourlyCost, testingLockStatus) == testingBodyType, testingMakeBrand #, testingBodyType, testingRego, testingColorType, testingNumSeats, testingHourlyCost, testingLockStatus

#test updating car lock status
def test_car_update():
    assert update_car_information(testingCarId, testingNewLockStatus) == testingNewLockStatus


#test adding new booking
def test_booking_add():
    assert create_booking_information(testingBookingId, testingCarId, testingUsername, testingBookStatus, testingStartTime, testingEndTime) == testingBookStatus 

#test updating new booking
def test_booking_update():
    assert update_booking_information(testingBookingId, testingAdminNote) == testingAdminNote



#the following are all deletion tests and will be expected to fail, as there will be nothing to return
#thus, they all have the xfail tag
#deleting the test booking
@pytest.mark.xfail
def test_booking_delete():
    assert delete_booking_information(testingBookingId) == testingBookingId

#deleting the test car
@pytest.mark.xfail
def test_car_delete():
    assert delete_car_information(testingCarId) == testingCarId

#deleting the test user
@pytest.mark.xfail
def test_user_delete():
    assert delete_user_information(testingUsername) == testingUsername

#deleting the test login
@pytest.mark.xfail
def test_login_delete():
    assert delete_login_information(testingUsername) == testingUsername
