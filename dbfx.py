from flask import session as flasksesh
import model
from sqlalchemy.sql import func
import random
from model import session as dbsesh


def get_user(email):
    """get user record to check password for logon"""
    user = dbsesh.query(model.User).filter_by(email = email).first()
    return user
    


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




def add_user_rating():
    """add or update movie rating while logged in"""
    pass



