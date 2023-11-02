from datetime import date
from flask import Flask, jsonify, request, render_template
import dbconnector as dbc
import json
import psycopg2


app = Flask(__name__)

'''
@app.route('/')
def home():
    return render_template('registration.html')
'''

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
    #print(responsedata)
    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200
    


# api to register a user and add their info to database
@app.route('/signup', methods=['POST'])
def register():
   
    json_data = jsonify(request.form)
    result = json_data.get_json()
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

if __name__ == '__main__':
    app.run()