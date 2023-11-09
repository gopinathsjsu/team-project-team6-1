from flask import Flask, jsonify, request, render_template
import json
import requests


app = Flask(__name__)
# @app.route("/openloginpage")
# def openloginpage():
#    return render_template('Login.html')
# @app.route("/")
# def openregisterpage():
#    return render_template("merge.html")
@app.route("/openupgradepage")
def openregisterpage():
   return render_template('upgrademembership.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
   if request.method == "POST":
        jsonrequest = json.dumps(request.form)
        print("jsonreq:",jsonrequest)
        r = requests.post('http://127.0.0.1:5000/signup', data=jsonrequest, headers= {'Content-Type': 'application/json'})
        print("r.text",r.text)
        #if successful
        #render_template(main.html)
        #else
        #error screen
   return render_template('registration.html')

@app.route('/', methods=['GET'])
def current_movies():
   if request.method == "GET":
        
        r = requests.get('http://127.0.0.1:5000/currentmovies')
        print(r)
        print(r.text)
        current_movies_json=json.loads(r.text)
        current_movies_featuring=current_movies_json[:4]
        r_upcoming = requests.get('http://127.0.0.1:5000/upcomingmovies')
        upcoming_movies_json=json.loads(r_upcoming.text)
        upcoming_movies_featuring=upcoming_movies_json[:4]
      #   it will also have upcoming 4movies
   return render_template("testhome.html",Featuring_movies=current_movies_featuring, upcoming_movies=upcoming_movies_featuring)

@app.route('/current_movies', methods=['GET'])
def all_current_movies():
   if request.method == "GET":
        
        r = requests.get('http://127.0.0.1:5000/currentmovies')
        print(r)
        print(r.text)
        current_movies_json=json.loads(r.text)
        current_movies_featuring=current_movies_json[:4]
        r_upcoming = requests.get('http://127.0.0.1:5000/upcomingmovies')
        upcoming_movies_json=json.loads(r_upcoming.text)
        upcoming_movies_featuring=upcoming_movies_json[:4]
   return render_template("testhome.html",movies=current_movies_json,Featuring_movies=current_movies_featuring, upcoming_movies=upcoming_movies_featuring)

@app.route('/upcoming_movies', methods=['GET'])
def upcoming_movies1():
   if request.method == "GET":
        
        r = requests.get('http://127.0.0.1:5000/currentmovies')
        r_upcoming = requests.get('http://127.0.0.1:5000/upcomingmovies')
        print(r)
        print(r.text)
        current_movies_json=json.loads(r.text)
        current_movies_featuring=current_movies_json[:4]
        upcoming_movies_json=json.loads(r_upcoming.text)
   return render_template("testhome.html",Featuring_movies=current_movies_featuring,upcoming_movie_all=upcoming_movies_json)
@app.route('/viewprofiledetails', methods=['POST', 'GET'])
def user_details():
      
      #   as of now its hardcoded need to figure our session user or current user
         jsonrequest={"username": "fhg@gmail.com"}
         print("jsonreq",json.dumps(jsonrequest))

         r = requests.post('http://127.0.0.1:5000/profileInfo', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})
         print("r.text",r.text)
         user_details=json.loads(r.text)
         print("userdetails",json.dumps(user_details))
         print("addressofusr",user_details['address'])

         return render_template("viewprofile.html", address=user_details['address'],fullname=user_details['fullname'],
                                membershiptilldate=user_details['membershiptilldate'],membershiptype=user_details['membershiptype'],
                                rewardpoints=user_details['rewardpoints'])
      
@app.route('/upgrademembership', methods=['POST'])
def upgrade_membership():
      
      #   as of now its hardcoded need to figure our session user or current user
         jsonrequest={"username": "fhg@gmail.com"}
         print("jsonreq",json.dumps(jsonrequest))

         r = requests.post('http://127.0.0.1:5000/upgradeToPremium', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})
         print("r.text",r.text)
         

         return "membership updated"
      
   

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)