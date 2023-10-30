from datetime import date
from flask import Flask, flash, jsonify, request, render_template
import dbconnector as dbc
import json
import psycopg2


app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# try:
#         db = psycopg2.connect("dbname=projectdb user=postgres password=divija@1998")
#         cursor = db.cursor()
# except:
#         print('Could not connect to the database.')

@app.route('/login')
def login():
   return render_template('Login.html')

# @app.route("/signin",methods=["POST"])
# def signin():
#     result = json.dumps(request.form)
#     requestdata = json.loads(result) 
#     # requestdata = request.get_json()

#     username = requestdata["username"]
#     password = requestdata["password"]

#     #use database connector object to connect to database and retrieve data
#     responsedata = dbc.checkLoginCredentials(username, password)
#     print(responsedata)
#     if "error" in responsedata[0]:
#         return responsedata, 400
#     return responsedata, 200



@app.route('/')
def home():
   return render_template('registration.html')

# api to register a user and add their info to database
@app.route('/register', methods=['POST'])
def register():
    
    # db = psycopg2.connect("dbname=projectdb user=postgres password=Divija@1998 host=localhost port=5433")
    # "host": "localhost",
    # "database": "divija",
    # "user": "postgres",
    # "password": "Divija@1998",
    # "port": "5433"
    # cursor = db.cursor()
    result = json.dumps(request.form)
    result = json.loads(result) 
    fullname = result['name']
    username = result['username']
    password = result['password']
    phoneno = result['phone_no']
    address = result['address']
    role = 'User'
    # response=dbc.registeruser(fullname, phoneno, address, username,password, role)
    response= dbc.registeruser(fullname, phoneno, address, username,password, role)
    print("respsonse:",response)
    data=response.get_json()
    
    success = data.get('success')
    
    
    
    if success:
    # #     # 'Registration was successful
      message = data.get('message')
      flash(message)
      return render_template('Login.html')
    # #     message = response['message']
    # #     # Perform any additional actions, such as redirecting or providing a success message
      
    else:
        error_details = data.get('error_details')
    # #     # Registration failed
    # #     error_message = response['error']
    # #     error_details = response['error_details']
    # #     # Handle the error, for example, return an error message
        return error_details
    # response = json.dumps(data)
    # response = json.loads(response) 
    # success=data['success']
    # message=data['message']
    # error_details=data['error_details']
    # error=data['error']
    # if success=='true':
        
    #   return message
    # else:
    #     print(error_details)
    #     return error
    
    # if "error" in responsedata:
    #     return responsedata, 400
    # return responsedata, 200
    # sql = '''INSERT INTO usertable (fullname, phonenumber, address, username, userpassword, userrole) VALUES (%s, %s, %s, %s, %s, %s);'''
    # cursor.execute('''select max(userid) from usertable;''')
    # max_id = cursor.fetchone()[0]
    # print(max_id)
    # print(type(max_id))
    # cursor.execute(sql, (fullname, phoneno, address, username, password, role))
    # db.commit()
    return response
if __name__ == '__main__':
    app.run()
    