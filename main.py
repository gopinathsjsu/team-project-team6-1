from datetime import date
from flask import Flask, request, jsonify
import dbconnector as dbc
import psycopg2


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
@app.route('/profileInfo', methods=['GET'])
def profileInfo():
    loginInfo = request.get_json()
    username = loginInfo['username']
    response = dbc.getProfileInfo(username)
    print('profile info - response : ', response)
    print(type(response))
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)