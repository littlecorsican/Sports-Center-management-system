from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


#app = Flask(__name__)

login_admin = Blueprint('login_admin', __name__)

from helpers import apology, admin_login_required, before_request, after_request


@login_admin.route("/admin/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        session.clear()

        if not request.form.get("username"):
            return redirect("/admin/login?status=2&msg=Please input username")

        elif not request.form.get("password"):
            return redirect("/admin/login?status=2&msg=Please input password")

        db = sqlite3.connect('database.db')

        user = request.form.get("username")

        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM admin WHERE username = ? ", (user,))

        rows = cur.fetchall()

        # Ensure username exists and password is correct
        if len(rows) < 1:
            return redirect("/admin/login?status=2&msg=Username does not exists")

        print(rows)
        print(rows[0])
        print(rows[0]["password"])

        if not check_password_hash(rows[0]["password"], request.form.get("password")):
            return redirect("/admin/login?status=2&msg=Incorrect Password")
        
        if rows[0]["approved"] == 0 :
            return redirect("/admin/login?status=2&msg=Your account has not been approved")

        # Remember which user has logged in
        session["user_id"] = rows[0]["admin_id"]
        session["user_type"] = "admin"
        session["username"] = rows[0]["username"]
        session["superadmin"] = rows[0]["superadmin"]
        session["approved"] = rows[0]["approved"]

        # Redirect user to home page
        return redirect("/admin/dashboard")


    else :

        print(type(session))

        if "user_id" in session:
            if session["user_type"] == "admin":
                return redirect("/admin/dashboard")
            return render_template("admin/login.html")

        return render_template("admin/login.html")


@login_admin.after_request
def response_processor(response):
    after_request(response)
    return response

# @login_admin.before_request
# def beforerequest():
#     before_request()