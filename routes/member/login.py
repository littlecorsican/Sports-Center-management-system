from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


#app = Flask(__name__)

login_member = Blueprint('login_member', __name__)

from helpers import member_login_required, before_request, after_request


@login_member.route("/member/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        session.clear()

        if not request.form.get("username"):
            return redirect("/member/login?status=2&msg=Please input username")

        elif not request.form.get("password"):
            return redirect("/member/login?status=2&msg=Please input password")

        db = sqlite3.connect('database.db')

        user = request.form.get("username")

        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? ", (user,))

        rows = cur.fetchall()

        # Ensure username exists and password is correct
        if len(rows) < 1:
            return redirect("/member/login?status=2&msg=Username does not exists")

        print(rows)
        print(rows[0])
        print(rows[0]["password"])

        if not check_password_hash(rows[0]["password"], request.form.get("password")):
            return redirect("/member/login?status=2&msg=Incorrect Password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_type"] = "member"
        session["username"] = rows[0]["username"]
        session["name"] = rows[0]["name"]

        # Redirect user to home page
        return redirect("/member/dashboard")


    else :

        if "user_id" in session:
            if session["user_type"] == "member":
                return redirect("/member/dashboard")
            return render_template("member/login.html")

        return render_template("member/login.html")


@login_member.after_request
def response_processor(response):
    after_request(response)
    return response

# @login_member.before_request
# def beforerequest():
#     before_request()