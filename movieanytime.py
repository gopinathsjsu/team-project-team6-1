from flask import Flask, jsonify, redirect, session, request, render_template, url_for
import json
import requests

app = Flask(__name__)

app.secret_key = 'fwe_5HvBK=9CvoqSD87xm'

# @app.route("/openloginpage")
# def openloginpage():
# #    return render_template('Login.html')
# @app.route("/")
# def openregisterpage():
#    return render_template("testhome.html")


@app.route("/openupgradepage")
def openregisterpage():
   return render_template('upgrademembership.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        jsonrequest = json.dumps(request.form)
        r = requests.post('http://127.0.0.1:5000/signin', data=jsonrequest, headers= {'Content-Type': 'application/json'})
        response = json.loads(r.text)
        if r.status_code == 200:
            session['username']=response[0]['username']
            session['ispremium']=response[0]['ispremium']
            session['userid']=response[0]['userid']
            session['rewardpoints']=response[0]['rewardpoints']
            return redirect(url_for('current_movies'))
        else:
            #show error message, maybe send a variable here to display in html with jinja
            return render_template('signin.html')
    return render_template('signin.html')

@app.route('/payment/<bookingid>', methods=['POST', 'GET'])
def payment(bookingid):
   userdetails = {}
   moviedetails = {}
   payment={}
   if session.get('userid'):
      userid = session['userid']
      userdetails['userid'] = userid
      jsonrequest={"userid": userid}
      r = requests.post('http://127.0.0.1:5000/getCardDetails', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})

      response = json.loads(r.text)
      if r.status_code == 200:
         userdetails["card_num"]=(response[0]['cardid'])%10000
      userdetails['email'] = session['username']
      userdetails['membership']= session['ispremium']
      userdetails['rewards']= session['rewardpoints']
   
   if(session.get('moviename') and session.get('multiplex') and session.get('theater')):
       moviedetails['moviename'] = session['moviename']
       moviedetails['multiplex'] = session['multiplex']
       moviedetails['theater'] = session['theater']
   else:
       #error remove this part afterwards
       moviedetails['moviename'] = 'Paw Patrol'
       moviedetails['multiplex'] = 'AMC SARATOGA'
       moviedetails['theater'] = 3

   jsonrequest={"bookingid": bookingid}
   moviedetails['bookingid'] = bookingid
   r = requests.post('http://127.0.0.1:5000/getTransactionDetails', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})

   response = json.loads(r.text)
   if r.status_code == 200:
       moviedetails['showdate'] =response[0]['showdate']
       moviedetails['showtime'] =response[0]['showtime']
       moviedetails['showingdetailid'] =response[0]['showingdetailid']
       moviedetails['noofseats'] =response[0]['array_length']
       moviedetails['seats'] =response[0]['seatid']
       payment['price'] = round(float(response[0]['price'].strip('$.')) * moviedetails['noofseats'] , 2)
       payment['discount'] = float(response[0]['discount'].strip('$.')) 
       payment['tax'] = round(float(payment['price']) * 0.05, 2)
       payment['fee'] = 2.50
       payment['total'] = round(payment['fee'] + payment['tax'] + payment['price'] - payment['discount'], 2)
   return render_template('payment.html', moviedetails =moviedetails, payment=payment, userdetails=userdetails)

@app.route('/bookingconfirmation', methods=['POST', 'GET'])
def bookingconfirmation():
   if request.method == "POST":
      jsonrequest = json.dumps(request.get_json())
      r = requests.post('http://127.0.0.1:5000/saveBooking', data=jsonrequest, headers= {'Content-Type': 'application/json'})
      if(r.status_code == 200):
         #session.pop('moviename')
         #session.pop('multiplex')
         #session.pop('theater')
         return jsonify({'response': r.text}), 200
      else:
          return jsonify({'response': r.text}), 400
          
   return render_template('confirmation.html')

@app.route('/bookingerror', methods=['POST', 'GET'])
def bookingerror():
   return render_template('error.html')


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
        #use session variables
        if session.get('username') :
            print(session['username'])
        
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
      
#       #   as of now its hardcoded need to figure our session user or current user
#          jsonrequest={"username": "fhg@gmail.com"}
#          print("jsonreq",json.dumps(jsonrequest))

#          r = requests.post('http://127.0.0.1:5000/profileInfo', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})
#          print("r.text",r.text)
#          user_details=json.loads(r.text)
#          print("userdetails",json.dumps(user_details))
#          print("addressofusr",user_details['address'])

#          return render_template("viewprofile.html", address=user_details['address'],fullname=user_details['fullname'],
#                                 membershiptilldate=user_details['membershiptilldate'],membershiptype=user_details['membershiptype'],
#                                 rewardpoints=user_details['rewardpoints'])
      jsonrequest={"username": "divijayuvraj30@gmail.com"}
      r1 = requests.post('http://127.0.0.1:5000/upcomingMovieBookings', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})
      print("r1.text",r1.text)
      futuremoviejson=json.loads(r1.text)
      r = requests.post('http://127.0.0.1:5000/pastMovieBookings', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})
      print("r.text",r.text)
      pastmoviejson=json.loads(r.text)
      r = requests.post('http://127.0.0.1:5000/profileInfo', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})
      print("r.text",r.text)
      user_details=json.loads(r.text)
      # print("userdetails",json.dumps(user_details))
      # print("addressofusr",user_details['address'])
      
      return render_template("commonprofile.html",futuremovieticket=futuremoviejson,pastmovieticket=pastmoviejson,address=user_details['address'],fullname=user_details['fullname'],
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
      
@app.route('/bookmovie', methods=['POST'])
def book_movies():
   if request.method =="POST":
      movieid = request.form.get('movieid')
      multiplexid = request.form.get('multiplexid')
      chosenDate = request.form.get('chosenDate')   
      
      print(movieid)       
      print(multiplexid)
      print(chosenDate)
      
      # movieid=6
      # multiplexid=14
      # chosenDate = '2023-11-03'
      
      data1 = {
         "movieid": movieid,
         "multiplexid":multiplexid,
         "chosenDate": chosenDate      
      }
      headers = {'Content-Type': 'application/json'}
      r = requests.post('http://127.0.0.1:5000/getmovietheaters', json=data1, headers=headers)
      print(r.text)
      theaters = json.loads(r.text)
   return render_template("bookmovie.html",theaters=theaters) 


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001,debug=True)