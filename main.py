from datetime import date
from flask import Flask, jsonify, request, render_template
import dbconnector as dbc
import json
import psycopg2


app =Flask(__name__)

@app.route('/login')
def login():
   return render_template('Login.html')

@app.route("/signin",methods=["POST"])
def signin():
    requestdata = request.get_json()

    username = requestdata["username"]
    password = requestdata["password"]

    #use database connector object to connect to database and retrieve data
    responsedata = dbc.checkLoginCredentials(username, password)
    print(responsedata)
    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200


try:
    db = psycopg2.connect("dbname=projectdb user=postgres password=postgres")
    cursor = db.cursor()
except:
    print('Could not connect to the database.')

@app.route('/')
def home():
   return render_template('registration.html')

# api to register a user and add their info to database
@app.route('/register', methods=['POST'])
def register():
    result = json.dumps(request.form)
    result = json.loads(result) 
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
    app.run()