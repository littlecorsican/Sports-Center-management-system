from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
import sqlite3

#app = Flask(__name__)

approve_admin = Blueprint('approve_admin', __name__)

from helpers import admin_login_required, before_request, after_request


@approve_admin.route("/admin/approve", methods=["GET", "POST"])
@admin_login_required
def orders():

    if request.method == "POST":
        
        admin_id = request.form.get("id")

        db = sqlite3.connect('database.db')

        db.row_factory = sqlite3.Row

        print(admin_id)
        sqlquery = "UPDATE admin SET approved = ? WHERE admin_id = ?"

        print(sqlquery)

        try:

            cur = db.cursor()
            cur.execute(sqlquery, (1,admin_id,))
            db.commit()

            return "1"
        except sqlite3.Error as er:
            print(er)
            return "0"

    else :

        if session["superadmin"] != 1 :
            return redirect("/admin/dashboard?msg=You have no priviledge to view this page!")

        db = sqlite3.connect('database.db')

        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM admin WHERE approved = 0 ")

        rows = cur.fetchall()

        length = len(rows)





        return render_template("admin/approve.html", rows=rows, length=length)


@approve_admin.route("/admin/dismiss", methods=["POST"])
@admin_login_required
def dismiss():

    admin_id = request.form.get("id")

    db = sqlite3.connect('database.db')

    db.row_factory = sqlite3.Row

    print(admin_id)
    sqlquery = "DELETE FROM admin WHERE admin_id = '" + admin_id + "'"

    print(sqlquery)

    try:

        cur = db.cursor()
        cur.execute(sqlquery)
        db.commit()

        return "1"
    except sqlite3.Error as er:
        print(er)
        return "0"


@approve_admin.after_request
def response_processor(response):
    after_request(response)
    return response

# @approve_admin.before_request
# def beforerequest():
#     before_request()