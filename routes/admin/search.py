from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context, jsonify
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


#app = Flask(__name__)

search_admin = Blueprint('search_admin', __name__)

from helpers import admin_login_required, before_request, after_request, sqlLiteRowToDict


@search_admin.route("/admin/search", methods=["GET", "POST"])
@admin_login_required
def search():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        joindate = request.form.get("joindate")

        print(username)
        print(email)
        print(joindate)
        

        queryArr = []
        sqlQuery = " WHERE "

        if username != "":
            queryArr.append("username = '" + username + "' ")

        if email != "":
            queryArr.append("email = '" + email + "' ")

        if joindate != "" and joindate != None:
            queryArr.append("joindate = '" + joindate + "' ")

        print(queryArr)

        if len(queryArr) == 0 :
            return redirect("search?status=2&msg=you did not input anything!")

        for index, val in enumerate(queryArr):
            print(index, val)
            if index > 0 :
                sqlQuery += " AND "
            sqlQuery += val

        print(sqlQuery)
        print("SELECT * FROM users" + sqlQuery)

        db = sqlite3.connect('database.db')

        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM users" + sqlQuery)

        rows = cur.fetchall()

        length = len(rows)

        if length == 0:
            return redirect("search?status=2&msg=No data found")
        else:
            return render_template("admin/search.html", rows = rows, length=length)

    else :
        length = 0
        return render_template("admin/search.html", length=0)

@search_admin.route("/admin/search/history", methods=["POST"])
@admin_login_required
def history():

    id = request.form.get("id")

    print(id)

    db = sqlite3.connect('database.db')

    db.row_factory = sqlite3.Row
    cur = db.cursor()
    
    sqlquery = "SELECT * FROM orders CROSS JOIN users ON orders.user_id = users.id CROSS JOIN venues ON orders.venue_id = venues.venue_id CROSS JOIN venue_type ON venues.venue_type = venue_type.type_id WHERE orders.user_id = " + str(id) 
    print(sqlquery)
    print(session["user_id"])
    cur.execute(sqlquery)

    rows = cur.fetchall()

    length = len(rows)
    print(length)

    cur.execute("SELECT * FROM venue_type ")

    venue_type = cur.fetchall()

    return sqlLiteRowToDict(rows)
    #return jsonify(rows=rows, length = length, venue_type = venue_type)



@search_admin.after_request
def response_processor(response):
    after_request(response)
    return response

# @login_member.before_request
# def beforerequest():
#     before_request()