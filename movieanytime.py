from flask import Flask, redirect, session, request, render_template, url_for
import json
import requests



app = Flask(__name__)
app.secret_key = 'fwe_5HvBK=9CvoqSD87xm'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        jsonrequest = json.dumps(request.form)
        r = requests.post('http://127.0.0.1:5000/signin', data=jsonrequest, headers= {'Content-Type': 'application/json'})
        #username = session['username']
        response = json.loads(r.text)
        if r.status_code == 200:
            session['username']=response[0]['username']
            session['ispremium']=response[0]['ispremium']
            session['userid']=response[0]['userid']
            return redirect(url_for('current_movies'))
        else:
            #show error message, maybe send a variable here to display in html with jinja
            return render_template('signin.html')
    return render_template('signin.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
   if request.method == "POST":
        jsonrequest = json.dumps(request.form)
        r = requests.post('http://127.0.0.1:5000/signup', data=jsonrequest, headers= {'Content-Type': 'application/json'})
        print(r.text)
        #if successful
        #render_template(main.html)
        #else
        #error screen
   return render_template('registration.html')

@app.route('/', methods=['GET'])
def current_movies():
   if request.method == "GET":
        #use session variables
        print(session['username'])
        current_movies = requests.get('http://127.0.0.1:5000/currentmovies')
        #print(current_movies.text)
        current_movies_json=json.loads(current_movies.text)
        upcoming_movies = requests.get('http://127.0.0.1:5000/upcomingmovies')
        #print(upcoming_movies.text)
        upcoming_movies_json=json.loads(upcoming_movies.text)
   return render_template("testhome.html",movies = current_movies_json)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)