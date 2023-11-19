from datetime import date
import json
from flask import Flask, request, jsonify
import dbconnector as dbc
import rsa

app = Flask(__name__)


# api to check username and password for login
@app.route("/signin",methods=["POST"])
def signin():
    '''
    headers = request.headers
    bearer = headers.get('Authorization')    # Bearer YourTokenHere
    if(bearer is None):
        return "No authorisation token", 401
    
    token = bearer.split()[1]  # YourTokenHere

    if token != "xyz-secret-key":
        return "Unauthorised user", 401
    '''
    requestdata = request.get_json()

    username = requestdata["username"]
    password = requestdata["password"]

    #use database connector object to connect to database and retrieve data
    responsedata = dbc.checkLoginCredentials(username, password)
    #print(responsedata)
    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to get currently showing movies
@app.route("/currentmovies",methods=["GET"])
def currentmovies():
    '''
    headers = request.headers
    bearer = headers.get('Authorization')    # Bearer YourTokenHere
    if(bearer is None):
        return "No authorisation token", 401
    
    token = bearer.split()[1]  # YourTokenHere

    if token != "xyz-secret-key":
        return "Unauthorised user", 401
    '''
    responsedata = dbc.getCurrentMovies()

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200
    
#api to get upcoming movies
@app.route("/upcomingmovies",methods=["GET"])
def upcomingmovies():
    responsedata = dbc.getUpcomingMovies()
    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200
    
#api to get all multiplexes  
@app.route("/multiplexlist",methods=["GET"])
def multiplexlist():
    responsedata = dbc.getMultiplexList()

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to get all the multiplexes, theater and date information for a particular movie
@app.route("/getmovietheaters",methods=["GET", "POST"])
def getmovietheaters():
    requestdata = request.get_json()

    movieid = requestdata["movieid"]
    multiplexid = requestdata["multiplexid"]
    date = requestdata["chosenDate"]
    responsedata = dbc.getShowingInfo(movieid, multiplexid, date)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to get seat allocation chart for a show
@app.route("/getseatmatrix", methods = ["POST"])
def getseatmatrix():
    requestdata = request.get_json()

    theaterid = requestdata["theaterid"]
    showdetailid = requestdata["showdetailid"]
    responsedata = dbc.getseatAllocation(theaterid, showdetailid)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to create a booking record
@app.route("/createbooking", methods=["POST"])
def createbooking():
    requestdata = request.get_json()

    seatid = requestdata["seatid"]
    showingdetailid = requestdata["showingdetailid"]
    userid = requestdata["userid"]
    responsedata = dbc.createBooking(seatid, showingdetailid, userid)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to fetch last 4 digits of card
@app.route("/getCardDetails", methods=["POST"])
def getCardDetails():
    requestdata = request.get_json()

    userid = requestdata["userid"]
    responsedata = dbc.getCardDetails(userid)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to save card details
@app.route("/saveBooking", methods=["POST"])
def saveBooking():
    requestdata = request.get_json()
    print(requestdata)
    card_number = requestdata["card_number"]
    cvv = requestdata["cvv"]
    exp = requestdata["exp"]
    rewardpointsused = requestdata["rewardpointsused"]
    email =requestdata["email"]
    moviedetails = eval(requestdata["moviedetails"].replace("'", "\""))
    payment =  eval(requestdata["payment"].replace("'", "\""))
    userdetails = eval(requestdata["userdetails"].replace("'", "\""))
    #if(userdetails is not None and "card_num" not in userdetails):

    if card_number != "":
        responsedata = dbc.saveCardDetails(card_number, cvv,exp, userdetails["userid"])
        print(responsedata)
    responsedata = dbc.completeBooking(moviedetails["bookingid"], payment, rewardpointsused, moviedetails["seats"])
    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200



#api to fetch booking details
@app.route("/getTransactionDetails", methods=["POST"])
def getTransactionDetails():
    requestdata = request.get_json()

    bookingid = requestdata["bookingid"]
    responsedata = dbc.getTransactionDetails(bookingid)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200


# api to register a user and add their info to database
@app.route('/signup', methods=['POST'])
def register():
    result = request.get_json()
    fullname = result['name']
    username = result['username']
    password = result['password']
    phoneno = result['phone_no']
    address = result['address']
    role = 'User'
    response= dbc.registeruser(fullname, phoneno, address, username,password, role)
    print("response:",response)
    data=response.get_json()
    data = dbc.registerUserMembership(username)
    print("Data : ",data)
    print(type(data))
    return data


# api to upgrade user's membership from Regular to Premium
@app.route('/upgradeToPremium', methods=['POST'])
def upgradeToPremium():
    loginInfo = request.get_json()
    username = loginInfo['username']
    response = dbc.upgradeMembership(username)
    print('upgrade - response : ', response)
    print(type(response))
    return response


# api to retrieve user details to display on profile - full name, address, membership type, membership valid till data, and rewards points
@app.route('/profileInfo', methods=['POST'])
def profileInfo():
    loginInfo = request.get_json()
    username = loginInfo['username']
    response = dbc.getProfileInfo(username)
    print('profile info - response : ', response)
    print(type(response))
    return response


# api to retrieve user's past movie bookings to display on profile
@app.route('/pastMovieBookings', methods=['GET','POST'])
def pastMovieBookings():
    loginInfo = request.get_json()
    username = loginInfo['username']
    response = dbc.getPastMovieBookings(username)
    print('past movie bookings - response : ', response)
    print(type(response))
    return response


# api to retrieve user's upcoming movie bookings to display on profile
@app.route('/upcomingMovieBookings', methods=['GET','POST'])
def upcomingMovieBookings():
    loginInfo = request.get_json()
    username = loginInfo['username']
    response = dbc.getUpcomingMovieBookings(username)
    print('upcoming movie bookings - response : ', response)
    print(type(response))
    return response

# api to retrieve user's 30 day movie history
@app.route('/moviesPast30Days', methods=['GET','POST'])
def moviesPast30Days():
    loginInfo = request.get_json()
    username = loginInfo['username']
    response = dbc.getMoviesPast30Days(username)
    print('30 day movie history - response : ', response)
    print(type(response))
    return response



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)