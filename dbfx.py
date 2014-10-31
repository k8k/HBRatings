from flask import session as flasksesh
import model
from sqlalchemy.sql import func
import random
from model import session as dbsesh


def get_user(email):
    """get user record to check password for logon"""
    user = dbsesh.query(model.User).filter_by(email = email).first()
    return user
    
def get_user_by_id(user_id):
    """get user record by user id"""
    user = dbsesh.query(model.User).filter_by(id = user_id).first()
    return user

def get_movie_by_name(movie_name):
    movie = dbsesh.query(model.Movie).filter_by(name=movie_name).first()
    return movie

def get_movie_by_id(movie_id):
    movie = dbsesh.query(model.Movie).get(movie_id)

def show_all_movies():
    movies = dbsesh.query(model.Movie).all()

    return movies

def create_new_user(email, password, age, zipcode):
    """add a new user to the db"""
    u = model.User()
    u.email = email
    u.password = password
    u.age = age
    # u.gender = gender
    # u.occupation = occupation
    u.zipcode = zipcode
    dbsesh.add(u)
    try:
        dbsesh.commit()
        return u
    except model.SQLAlchemyError:
        return "user already exists, try again"


def log_on(email, password):
    """verify user credentials, add something to whatever that
    g thing is that is supposed to help us"""
    pass


def view_all_users():
    """view all users"""
    pass


def show_random_user_ratings():
    """return a list of movies and ratings given by this user"""
    our_range = dbsesh.query(model.User.id).all()
    # print our_range

    clean_list =[]

    for i in range(len(our_range)):
        clean_list.append(our_range[i][0])

    # print clean_list

    users_to_show = []

    for i in range(10):
        random_user = random.choice(clean_list)
        users_to_show.append(random_user)

    user_objects = []
    for uid in users_to_show:
        user_object = dbsesh.query(model.User).get(uid)
        user_objects.append(user_object)

    print len(user_objects)
    return (user_objects)

     # "in random user function"




def dbadd_user_rating(user, rating, movie):
    """add or update movie rating while logged in"""

    # print user
    # print movie

    user = dbsesh.query(model.User).filter_by(email=user).first()
    movie = dbsesh.query(model.Movie).filter_by(name=movie).first()

    # print dir(user)
    # print user.ratings
    # print movie
    # reviewed_movies = []
    # print reviewed_movies
    # rating = r.rating

    # for i in range(len(user.ratings)):
    #     reviewed_id = user.ratings[i].movie_id
    #     reviewed_movies.append(reviewed_id)

    # if movie.id in reviewed_movies:

    # if len(user.ratings)>1:
    #     for i in range(len(user.ratings)):
    #         if movie.id == user.ratings[i].movie_id:
    #             user.ratings[i].rating = rating

    # print "user.ratings----------------------------\n", user.ratings[0].movie_id

    # print "move----------------------------\n", dir(movie)

    r = model.Rating()
    r.user_id = user.id
    r.rating = rating
    r.movie_id = movie.id

    dbsesh.add(r)
    dbsesh.commit()
    return r




