from datetime import date
from flask import Flask, jsonify, request, render_template
import dbconnector as dbc


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


if __name__== "__main__":
    app.run()