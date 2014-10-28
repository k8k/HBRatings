from flask import Flask, render_template, redirect, request
import model
from model import session
import dbfx

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()

    return render_template("user_list.html", user_list=user_list)

@app.route("/logon")
def logon():
    check_user()



@app.route("/checkuser")
def check_user():
    # u = dbfx.create_new_user()
    # print u

    email = request.args.get("user_email")
    print email
    # x = session.query(model.User).filter_by(email=u.email).all()
    # print x
    # print u.email
    # print type(u.email)
    # return "got here"

    # checks = []
    check = session.query(model.User).filter_by(email=email).all()

    if len(check)<1:
        return render_template("newuser.html")
    else:
        return "that user already exists! please try again."
    print check
    print type(check)
    return "hi"
    # new_user = True

    # for obj in check:
    #     if u.email == obj.email:
    #         new_user = False
    #     else:
    #         new_user = True
    #     return new_user
    # if new_user == True:
    #     return "we have a new user"
    #     redirect("/newuser")
    # else:
        # return "email password combo not found"

    # if email != check.email:
    #     return "Great"
    # else:
    #     return "User already exists."



    # checks.append(check)

@app.route("/newuser")
def newuser():
    email = request.args.get("nuser_email")
    password = request.args.get("nuser_password")
    new_u = dbfx.create_new_user(email, password)

    return new_u.email
  

if __name__ == "__main__":
    app.run(debug = True)