from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
import sqlite3

#app = Flask(__name__)

dashboard_member = Blueprint('dashboard_member', __name__)

from helpers import member_login_required, before_request, after_request


@dashboard_member.route("/member/dashboard", methods=["GET"])
@member_login_required
def dashboard():

    db = sqlite3.connect('database.db')

    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("SELECT * FROM config WHERE key = 'announcement' LIMIT 1")

    rows = cur.fetchone()

    cur.execute("SELECT * FROM venue_type")

    venue_type = cur.fetchall()

    cur.execute("SELECT * FROM config")

    config = cur.fetchall()

    print(rows)

    
    return render_template("member/dashboard.html", rows=rows, venue_type=venue_type, config=config)




@dashboard_member.after_request
def response_processor(response):
    after_request(response)
    return response

# @dashboard_member.before_request
# def beforerequest():
#     before_request()