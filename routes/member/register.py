from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from datetime import date
import re

#app = Flask(__name__)

register_member = Blueprint('register_member', __name__)

from helpers import before_request, after_request


@register_member.route("/member/register", methods=["GET", "POST"])
def register():

    print("1")
    regex = "[a-zA-Z0-9]{9}"

    if request.method == "POST":

        print("2")

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirmation = request.form.get("confirmation")
        name = request.form.get("name")

        if not request.form.get("username"):
            return redirect("/member/register?status=2&msg=Please input username")

        elif not request.form.get("password"):
            return redirect("/member/register?status=2&msg=Please input password")

        elif not request.form.get("confirmation"):
            return redirect("/member/register?status=2&msg=Please input reinput password")
    
        elif not request.form.get("name"):
            return redirect("/member/register?status=2&msg=Please input name")

        elif re.search(regex, password) == None :
            return redirect("/member/register?status=2&msg=Please input password with alhpaberts and numbers of minimum 9 letters only")

        elif request.form.get("confirmation") != request.form.get("password") :
            return redirect("/member/register?status=2&msg=Password and confirm password not the same")

        print("3")

        db = sqlite3.connect('database.db')
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? ", (username,))

        rows = cur.fetchall()

        if len(rows) > 0:
            return redirect("/member/register?status=2&msg=account with that username already exists!")

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


        db.execute('INSERT INTO users (username,password, email, join_date, name) VALUES (?,?,?,?,?) ' ,(username,hash, email, todaydate, name) )
        db.commit()

        db.close()

        print("succesfully created new account!")


        # Redirect user to home page
        return redirect("/member/register?status=1")

    else :
        return render_template("member/register.html", regex=regex)


# @register_member.after_request
# def response_processor(response):
#     after_request(response)
#     return response

# @register_member.before_request
# def beforerequest():
#     before_request()