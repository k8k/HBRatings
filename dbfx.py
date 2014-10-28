from flask import session
import model


def check_for_user(email):
    """check if user already exists before creating new user"""
    pass


def create_new_user(email, password):
    """add a new user to the db"""
    u = model.User()
    u.email = email
    u.password = password
    # u.age = age
    # u.gender = gender
    # u.occupation = occupation
    # u.zipcode = zipcode
    model.session.add(u)
    model.session.commit()
    return u


def log_on(email, password):
    """verify user credentials, add something to whatever that
    g thing is that is supposed to help us"""
    pass


def view_all_users():
    """view all users"""
    pass


def show_user_ratings(user):
    """return a list of movies and ratings given by this user"""
    pass


def add_user_rating():
    """add or update movie rating while logged in"""
    pass



