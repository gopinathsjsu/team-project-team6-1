from datetime import date
from flask import Flask, jsonify, request
import dbconnector as dbc


app =Flask(__name__)

@app.route("/login",methods=["POST"])
def signin():
    requestdata = request.get_json()

    #use database connector object to connect to database and retrieve data
    responsedata = dbc.checkLoginCredentials(requestdata)
    if "error" in responsedata[0]:
        return responsedata, 400
    return responsedata, 200


if __name__== "__main__":
    app.run()