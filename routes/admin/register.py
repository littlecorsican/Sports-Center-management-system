from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from datetime import date
import re

#app = Flask(__name__)

register_admin = Blueprint('register_admin', __name__)

from helpers import admin_login_required, before_request, after_request


@register_admin.route("/admin/register", methods=["GET", "POST"])
def register():

    print("1")
    regex = "[a-zA-Z0-9]{9}"

    if request.method == "POST":

        print("2")

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirmation = request.form.get("confirmation")

        if not request.form.get("username"):
            return redirect("/admin/register?status=2&msg=Please input username")

        elif not request.form.get("password"):
            return redirect("/admin/register?status=2&msg=Please input password")

        elif not request.form.get("confirmation"):
            return redirect("/admin/register?status=2&msg=Please input reinput password")

        elif re.search(regex, password) == None :
            return redirect("/admin/register?status=2&msg=Please input password with alhpaberts and numbers of minimum 9 letters only")

        elif request.form.get("confirmation") != request.form.get("password") :
            return redirect("/admin/register?status=2&msg=Password and confirm password not the same")

        print("3")

        db = sqlite3.connect('database.db')
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM admin WHERE username = ? ", (username,))

        rows = cur.fetchall()

        if len(rows) > 0:
            return redirect("/admin/register?status=2&msg=account with that username already exists!")

        # salt = os.urandom(32) # Remember this

        # #salt = os.environ.get("API_KEY")

        # hash = hashlib.pbkdf2_hmac(
        #     'sha256',
        #     password.encode('utf-8'),
        #     salt,
        #     100000
        # )

        hash = generate_password_hash(password)

        print (hash)

        today = date.today()
        todaydate = today.strftime("%d/%m/%Y")


        db.execute('INSERT INTO admin (username,password, email, join_date) VALUES (?,?,?,?) ' ,(username,hash, email, todaydate) )
        db.commit()

        db.close()

        print("succesfully created new account!")


        # Redirect user to home page
        return redirect("/admin/register?status=1")

    else :
        return render_template("admin/register.html", regex=regex)


# @register_admin.after_request
# def response_processor(response):
#     after_request(response)
#     return response

# @register_admin.before_request
# def beforerequest():
#     before_request()