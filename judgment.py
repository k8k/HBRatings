from flask import Flask, render_template, redirect, request, g, session as flasksesh
import model
from model import session as dbsesh 
import dbfx
import random

app = Flask(__name__)
app.secret_key = "hgfutrdiuytdr576ryu"

@app.before_request
def get_user_info():
    g.user_email = flasksesh.get("email")

@app.route("/")
def index():
    if g.user_email:
        return redirect("/users/home")
    else:
        return render_template("base.html")

@app.route("/logon")
def logon():
    # check_user()
    return render_template("logon.html")


@app.route("/logon/userlogin", methods=['POST'])
def check_user():
    email = request.form.get("user_email")
    print email

    check = dbsesh.query(model.User).filter_by(email=email).all()

    if len(check)<1:
        return render_template("newuser.html")
    else:
        email = request.form.get("user_email")
        dbuser = dbfx.get_user(email)
        password = request.form.get("user_password")
        if password != dbuser.password:
            return "Wrong password, try again"
        else:
            flasksesh["email"] = dbuser.email
            flasksesh["user_id"] = dbuser.id
            print flasksesh
            return redirect("/") 

@app.route("/users/home")
def user_home():
    return render_template("user_home.html", user_email=g.user_email)


@app.route("/newuser")
def newuser():
    return render_template("newuser.html")

@app.route("/newuser/add", methods=['POST'])
def create_new_user():

    email = request.form.get("new_user_email")

    check = dbsesh.query(model.User).filter_by(email=email).all()

    if len(check)<1:
        email = request.form.get("new_user_email")
        password = request.form.get("new_user_password")
        age = int(request.form.get("new_user_age"))
        zipcode = request.form.get("new_user_zipcode")
        print email, password, age, zipcode

        new_user = dbfx.create_new_user(email, password, age, zipcode)

        flasksesh["email"] = email
        flasksesh["password"] = password
        flasksesh["user_id"] = new_user.id
        print flasksesh
        return redirect("/")
    else:
        
        return redirect("/logon")

@app.route("/users/ratings/random")
def show_random_user_ratings():
    users = dbfx.show_random_user_ratings()

    print users
    
    ratings_list = []
    
    for i in range(len(users)):
        user = users[i]
        print user
    
        try:
            rating = random.choice(user.ratings)
            # moviename = rating.movie.name
            ratings_list.append(rating)
        except IndexError:
            continue
    
    print ratings_list

    return render_template("ratings.html", rating_list=ratings_list)


@app.route("/users/<int:user_id>/ratings/all")
def show_all_ratings_for_user(user_id):
    user = dbfx.get_user_by_id(user_id)
    print dir(user)

    user_ratings = user.ratings

    return render_template("user_ratings.html", user_ratings=user_ratings)


@app.route("/movies/<movie_name>")
def movie_detail(movie_name):
    movie = dbfx.get_movie_by_name(movie_name)
    # print movie.name
    print flasksesh
    ratings = movie.ratings
    rating_nums = []
    user_rating = None

    for r in ratings:
        if r.user_id == flasksesh["user_id"]:
            user_rating = r
        rating_nums.append(r.rating)
    print rating_nums
    # avg_rating = float(sum(rating_nums))/len(rating_nums)
    #prediction
    user = dbsesh.query(model.User).get(flasksesh['user_id'])
    prediction = None
    if not user_rating:
        prediction = user.predict_rating(movie)
        effective_rating = prediction
    else:
        effective_rating = user_rating.rating

    the_eye = dbsesh.query(model.User).filter_by(email="theeye@ofjudgment.com").one()
    eye_rating = dbsesh.query(model.Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie)
    else:
        eye_rating = eye_rating.rating

    difference = abs(eye_rating - effective_rating)

    messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot.",]

    beratement = messages[int(difference)]

    return render_template("movie_info.html", movie=movie, prediction=prediction, beratement=beratement)


@app.route("/movies")
def all_movies():
    
    movies = dbfx.show_all_movies()
    # print movies
    return render_template("all_movies.html", movie_list=movies)


@app.route("/addrating/<movie_name>", methods=['POST', 'GET'])
def add_new_user_rating(movie_name):
    # print movie_name
    rating = request.form.get("new_user_rating")
    user_email = g.user_email

    # print movie_name
    # print user_email
    # print rating

    new_rating = dbfx.dbadd_user_rating(user_email, str(rating), movie_name)
    print new_rating
    return redirect("/movies")

@app.route("/logout")
def user_logout():
    flasksesh.clear()
    print flasksesh
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)