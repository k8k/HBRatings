from flask import Flask, render_template, redirect, request, g, session as flasksesh
import model
from model import session as dbsesh
import dbfx
import random

app = Flask(__name__)
app.secret_key = "hgfutrdiuytdr576ryu"

# @app.before_request
# def get_user_info():
#     pass

@app.route("/")
def index():
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
            flasksesh["password"] = dbuser.password
            print flasksesh
            return render_template("user_home.html", user_email=flasksesh["email"]) 


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
        print flasksesh
        return "Successfully added %s, age %r" % (new_user.email, new_user.age)
    else:
        
        return redirect("/logon")

@app.route("/users/ratings/random")
def show_random_user_ratings():
    users = dbfx.show_random_user_ratings()

    print users


  
    ratings_list = []
    # print dir(debug.ratings[0])
    # print dir(debug.ratings[0].movie)
    # print debug.ratings[0].movie.name
    for i in range(len(users)):
        user = users[i]
        print user
        
        rating = random.choice(user.ratings)
        moviename = rating.movie.name
        ratings_list.append(rating)
    
    print ratings_list

    # movieids = []

    # for i in range(len(debug.ratings)):
    #     movieid = debug.ratings[i].movie_id
    #     movieids.append(movieid)

    # print movieids 

    # for i in range(len(movieids)):
            

        # whatever = movieids[i].movies.name
        # print whatever


    # for user in users:
    #     for rating in user.ratings:
    #         print user.ratings.movie_id

    return render_template("ratings.html", rating_list=ratings_list)



@app.route("/logout")
def user_logout():
    flasksesh = {}
    print flasksesh
    return redirect("/")




if __name__ == "__main__":
    app.run(debug = True)