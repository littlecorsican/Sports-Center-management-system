from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


#app = Flask(__name__)

history_member = Blueprint('history_member', __name__)

from helpers import member_login_required, before_request, after_request


@history_member.route("/member/history", methods=["GET"])
@member_login_required
def history():

    # if request.method == "POST":

    #     return "1"


    # else :


    db = sqlite3.connect('database.db')

    db.row_factory = sqlite3.Row
    cur = db.cursor()
    
    sqlquery = "SELECT * FROM orders CROSS JOIN venues ON orders.venue_id = venues.venue_id CROSS JOIN venue_type ON venues.venue_type = venue_type.type_id WHERE user_id = " + str(session["user_id"])
    print(sqlquery)
    print(session["user_id"])
    cur.execute(sqlquery)

    rows = cur.fetchall()

    # print(rows[0]['payment_method'])

    length = len(rows)

    cur.execute("SELECT * FROM venue_type ")

    venue_type = cur.fetchall()


    return render_template("member/history.html", rows = rows, length=length, venue_type=venue_type)


@history_member.after_request
def response_processor(response):
    after_request(response)
    return response

# @login_member.before_request
# def beforerequest():
#     before_request()