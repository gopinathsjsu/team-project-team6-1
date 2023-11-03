from flask import Flask, jsonify, request, render_template
import json
import requests



app = Flask(__name__)

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
        current_movies = requests.get('http://127.0.0.1:5000/currentmovies')
        print(current_movies.text)
        current_movies_json=json.loads(current_movies.text)
        upcoming_movies = requests.get('http://127.0.0.1:5000/upcomingmovies')
        print(upcoming_movies.text)
        upcoming_movies_json=json.loads(upcoming_movies.text)
   return render_template("testhome.html",movies = current_movies_json)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)