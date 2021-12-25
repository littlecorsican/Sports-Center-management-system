from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
import sqlite3
from datetime import datetime


#app = Flask(__name__)

order_admin = Blueprint('order_admin', __name__)

from helpers import admin_login_required, before_request, after_request


@order_admin.route("/admin/orders", methods=["GET", "POST"])
@admin_login_required
def orders():

    if request.method == "POST":
        return ""

    else :

        date = request.args.get('date')
        type = request.args.get('type')
        paid = request.args.get('paid')

        

        if date == None or date == "" :
            print("none")
            date = datetime.today().strftime('%d/%m/%Y')
        else:
            dateSplit = date.split("-")
            date = dateSplit[2] + "/" + dateSplit[1] + "/" + dateSplit[0]
            
        print(date)
        print(type)
        print(paid)

        queryArr = []
        sqlQuery = " WHERE "

        if date != None:
            queryArr.append("orders.start_date > '" + date + " 00:00:00' AND orders.end_date < '" + date + " 23:59:59'")


        if type != "All" and type != None:
            queryArr.append("venue_type.type_id = " + type + " ")

        if paid == "paid":
            queryArr.append("paid = TRUE ")
        elif paid == "unpaid": 
            queryArr.append("paid = FALSE ")


        print(queryArr)

        for index, val in enumerate(queryArr):
            print(index, val)
            if index > 0 :
                sqlQuery += " AND "
            sqlQuery += val

        print(sqlQuery)


        db = sqlite3.connect('database.db')

        db.row_factory = sqlite3.Row
        cur = db.cursor()
        # cur.execute("SELECT * FROM orders WHERE start_date > ? ", (date,) )
        cur.execute("SELECT * FROM orders CROSS JOIN users ON orders.user_id = users.id CROSS JOIN venues ON orders.venue_id = venues.venue_id CROSS JOIN venue_type ON venues.venue_type = venue_type.type_id" + sqlQuery)

        rows = cur.fetchall()

        length = len(rows)

        cur.execute("SELECT * FROM venue_type ")

        venue_type = cur.fetchall()


        return render_template("admin/orders.html", rows = rows, length=length, venue_type=venue_type)


@order_admin.route("/admin/orders/cancel", methods=["POST"])
@admin_login_required
def cancel():

    # if request.method == "POST":

    id = request.form.get("id")

    print(id)

    db = sqlite3.connect('database.db')

    try:
        
        db.execute("UPDATE orders SET cancelled = ? WHERE order_id = ?" ,(1, id) )
        db.commit()
        db.close()

        return "Updated successfully"
    except sqlite3.Error as er:
        print(er)
        return "Fail to update"

    # else :
    #     return "invalid request"


@order_admin.after_request
def response_processor(response):
    after_request(response)
    return response

# @order_admin.before_request
# def beforerequest():
#     before_request()