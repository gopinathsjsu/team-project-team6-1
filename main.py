from datetime import date
from flask import Flask, request
import dbconnector as dbc
import psycopg2


app = Flask(__name__)

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

    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200




# api to register a user and add their info to database
@app.route('/signup', methods=['POST'])
def signup():
    try:
        db = psycopg2.connect("dbname=movieanytime user=postgres password=postgres")
        cursor = db.cursor()
    except:
        print('Could not connect to the database.')

    result = request.get_json()

    fullname = result['name']
    username = result['username']
    password = result['password']
    phoneno = result['phone_no']
    address = result['address']
    role = 'User'
    sql = '''INSERT INTO usertable (userid, fullname, phonenumber, address, username, userpassword, userrole) VALUES (%s, %s, %s, %s, %s, %s, %s);'''
    cursor.execute('''select max(userid) from usertable;''')
    max_id = cursor.fetchone()[0]
    print(max_id)
    print(type(max_id))
    cursor.execute(sql, (max_id + 1, fullname, phoneno, address, username, password, role))
    db.commit()
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)