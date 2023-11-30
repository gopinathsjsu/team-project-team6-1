from datetime import date
import json
from flask import Flask, request, jsonify
import dbconnector as dbc
import rsa
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

#api to add/update movie in schedule
@app.route("/addMovie", methods=["POST"])
def addMovie():
    requestdata = request.get_json()

    name = requestdata["moviename"]
    runtimeminutes = requestdata["runtimeminutes"]
    releasedate = requestdata["releasedate"]
    endshowingdate = requestdata["endshowingdate"]
    poster = requestdata["poster"]
    if 'movieid' in requestdata:
        movieid = requestdata["movieid"]
        responsedata = dbc.updateMovie(movieid, runtimeminutes, endshowingdate, poster)
    else:
        responsedata = dbc.createMovie(name, runtimeminutes, releasedate, endshowingdate, poster)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to Add and update location
@app.route("/addLocation", methods=["POST"])
def addLocation():
    requestdata = request.get_json()

    city = requestdata["city"]
    postalcode = requestdata["postalcode"]
    noofmultiplex = requestdata["noofmultiplex"]
    if 'locationid' in requestdata:
        locationid = requestdata["locationid"]
        responsedata = dbc.updateLocation(locationid, noofmultiplex)
    else:
        responsedata = dbc.createLocation(city, postalcode, noofmultiplex)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200


#api to Add and update multiplex in schedule
@app.route("/addMultiplex", methods=["POST"])
def addMultiplex():
    requestdata = request.get_json()

    name = requestdata["multiplexname"]
    locationid = requestdata["locationid"]
    address = requestdata["address"]
    nooftheaters = requestdata["nooftheaters"]
    if 'multiplexid' in requestdata:
        multiplexid = requestdata["multiplexid"]
        responsedata = dbc.updateMultiplex(multiplexid, name, address, nooftheaters)
    else:
        responsedata = dbc.createMultiplex(name, locationid, address, nooftheaters)

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

#api to Add theaters in schedule and add respective seats in seat table
@app.route("/addTheater", methods=["POST"])
def addTheater():
    requestdata = request.get_json()
    multiplexid = requestdata["multiplexid"]
    noofseats = requestdata["noofseats"]
    theaternumber = requestdata["theaternumber"]
    noofrows = requestdata["noofrows"]
    noofcolumns = requestdata["noofcolumns"]
    movieid = requestdata["movieid"]# comma seperated string
    price = requestdata["price"]# comma seperated string
    showtimes = requestdata["showtimes"]# string of set
    
    if 'theaterid' in requestdata:
        theaterid = requestdata["theaterid"]
        responsedata = dbc.updateTheater(theaternumber, theaterid)
        if 'showingid' in requestdata:
            showingid = requestdata["showingid"]
            data, showingdetails = dbc.updateshowingmaster(movieid, showtimes, theaterid, noofseats, showingid)
            data, seats = dbc.getseats(theaterid)
            dbc.createSeatDetails(seats, showingdetails)

    else:
        responsedata = dbc.createTheater(multiplexid, noofseats, theaternumber, noofrows, noofcolumns, movieid, showtimes, price)
        data,seats = dbc.createSeat(responsedata[0]["theaterid"], noofrows, noofcolumns)
        data, showingdetails = dbc.createshowingmaster(movieid, showtimes, price, responsedata[0]["theaterid"], noofseats, seats)
                            
        dbc.createSeatDetails(seats, showingdetails)
    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200

#api to get all theater for a given multiplex
@app.route("/getalltheaters",methods=["POST"])
def getalltheaters():
    requestdata = request.get_json()

    multiplexid = requestdata["multiplexid"]
    responsedata = dbc.getTheaterInfo(multiplexid)

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200


#api to Delete theaters in schedule and respective seats in seat table
@app.route("/removeTheater", methods=["POST"])
def removeTheater():
    requestdata = request.get_json()
    theaterid = requestdata["theaterid"]
    
    responsedata = dbc.deleteshowingmaster(theaterid)
    responsedata = dbc.deleteseat(theaterid)
    responsedata = dbc.deleteTheater(theaterid)
    
    if len(responsedata) == 0:
        return responsedata, 200
    return responsedata, 400

#to remove a movie from theater
@app.route("/removeMovie", methods=["POST"])
def removeMovie():
    requestdata = request.get_json()
    showingid = requestdata["showingid"]
    
    responsedata, showingdetailid = dbc.deleteshowingmaster1(showingid)
    responsedata = dbc.deleteseat1(showingdetailid)
    
    if len(responsedata) == 0:
        return responsedata, 200
    return responsedata, 400

#api to remove a showtime
@app.route("/removeShowtime", methods=["POST"])
def removeShowtime():
    requestdata = request.get_json()
    showingid = requestdata["showingid"]
    showtime = requestdata["showtime"]
    
    responsedata, showingdetailid  = dbc.deleteshowtime(showingid, showtime)
    responsedata = dbc.deleteseat1(showingdetailid)
    
    if len(responsedata) == 0:
        return responsedata, 200
    return responsedata, 400


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
    print("data in main.py",data)
    if("error" in data ):
        return data
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

# api to delete user's movie booking
@app.route('/cancelBooking', methods=['DELETE'])
def cancelBooking():
    bookingInfo = request.get_json()
    bookingId = bookingInfo['bookingid']
    response = dbc.releaseSeats(bookingId)
    response = dbc.cancelBooking(bookingId)
    print('cancel movie bookings - response : ', response)
    print(type(response))
    return response

# api to retrieve multiplexes by location
@app.route('/retrieveMultiplexes', methods=['GET'])
def retrieveMultiplexes():
    locationInfo = request.get_json()
    locationId = locationInfo['locationid']
    response = dbc.getMultiplexesByLocation(locationId)
    print('retrieve multiplexes by location - response : ', response)
    print(type(response))
    return response


# api to retrieve movies which have played in the past 90 days
@app.route('/retrieveMoviesPlayedPast90Days', methods=['GET'])
def retrieveMoviesPlayedPast90Days():
    response = dbc.getMoviesPlayedPast90Days()
    print('retrieve movies which have played in the past 90 days - response : ', response)
    print(type(response))
    return response


# api to retrieve all cities in db
@app.route('/retrieveAllCities', methods=['GET','POST'])
def retrieveAllCities():
    response = dbc.getAllCities()
    print('retrieve all cities in db - response : ', response)
    print(type(response))
    return response


# api to retrieve theater occupancy info by location over past 30, 60, and 90 days
@app.route('/theaterOccupancyInfoByLocation', methods=['POST'])
def theaterOccupancyInfoByLocation():
    locationInfo = request.get_json()
    locationid = locationInfo['locationid']
    print("locationid in main",locationid)
    response = dbc.theaterOccupancyByLocation(locationid)
    print('retrieve theater occupancy info by location over past 30, 60, 90 days : ', response)
    print(type(response))
    return response

# api to retrieve theater occupancy info by moviename over past 30, 60, and 90 days
@app.route('/theaterOccupancyInfoByMovie', methods=['POST'])
def theaterOccupancyInfoByMovie():
    movieInfo = request.get_json()
    moviename = movieInfo['moviename']
    print("moviename in main",moviename)
    response = dbc.theaterOccupancyByMovie(moviename)
    print('retrieve theater occupancy info by movie over past 30, 60, 90 days : ', response)
    print(type(response))
    return response

# api to configure discount prices for showings
@app.route('/configDiscount', methods=['GET','POST'])
def configDiscounts():
    discountInfo = request.get_json()
    movieid = discountInfo['movieid']
    discount = discountInfo['discount']
    showdate = discountInfo['showdate']
    response = dbc.configDiscount(movieid,discount,showdate)
    print('configure discount price for movie showing on Tuesday or pre-6pm : ', response)
    print(type(response))
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)