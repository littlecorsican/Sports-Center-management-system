from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
import sqlite3
from datetime import datetime

#app = Flask(__name__)

dashboard_admin = Blueprint('dashboard_admin', __name__)

from helpers import apology, admin_login_required, before_request, after_request


@dashboard_admin.route("/admin/dashboard", methods=["GET"])
@admin_login_required
def dashboard():

    #todayDate = datetime.today().strftime('%Y-%m-%d')
    startDate = datetime.today().strftime("%d/%m/%Y 00:00:00")
    endDate = datetime.today().strftime("%d/%m/%Y 23:59:59")

    print(startDate)
    print(endDate)
    print(str(startDate))
    print(str(endDate))


    db = sqlite3.connect('database.db')

    db.row_factory = sqlite3.Row
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) as total FROM orders WHERE start_date > '" + str(startDate) + "' AND " + "end_date < '" + str(endDate) + "'")
    order1 = cur.fetchall()

    cur.execute("SELECT COUNT(*) as total FROM orders WHERE start_date > '" + str(startDate) + "' AND " + "end_date < '" + str(endDate) + "' AND cancelled = 0")
    order2 = cur.fetchall()

    cur.execute("SELECT COUNT(*) as total FROM orders WHERE start_date > '" + str(startDate) + "' AND " + "end_date < '" + str(endDate) + "' AND cancelled = 0")
    order3 = cur.fetchall()

    cur.execute("SELECT COUNT(*) as total FROM admin WHERE approved = 0")
    order4 = cur.fetchall()

    cur.execute("SELECT COUNT(*) as total FROM users WHERE join_date > '" + str(startDate) + "' AND " + "join_date < '" + str(endDate) + "'")
    order5 = cur.fetchall()

    return render_template("admin/dashboard.html", order1=order1, order2=order2, order3=order3, order4=order4, order5=order5)


@dashboard_admin.after_request
def response_processor(response):
    after_request(response)
    return response

# @dashboard_admin.before_request
# def beforerequest():
#     before_request()