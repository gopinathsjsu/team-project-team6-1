from datetime import date
from flask import Flask, render_template, request
import dbconnector as dbc


app =Flask(__name__)



@app.route("/")
def home():
    movies = dbc.readdata("movie", "*", "current_movies")
    return render_template("homepage.html", movies = movies)

@app.route("/movies/<moviename>", methods=["POST", "GET"])
def bookmovie(moviename):
    if request.method == "POST":
        moviedate = request.form.get("showdate")
        multiplex = request.form.get("theaters")
        print("Multiplex = ", multiplex)
    else:
        moviedate = date.today()
        multiplex = 1
    showing = dbc.fetchshowingdetails(moviename, moviedate, multiplex)
    return render_template("bookmovie.html", moviename=moviename, showings= showing)


if __name__== "__main__":
    app.run()