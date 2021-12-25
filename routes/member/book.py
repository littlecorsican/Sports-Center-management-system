from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from datetime import datetime, timedelta

#app = Flask(__name__)

book_member = Blueprint('book_member', __name__)

from helpers import member_login_required, before_request, after_request, isTimeFormat


@book_member.route("/member/book", methods=["GET", "POST"])
@member_login_required
def book():

    if request.method == "POST":

        return "1"

        # opening = request.form.get("opening")
        # closing = request.form.get("closing")
        # offdays = listToString(request.form.getlist("offdays"))


        # openingTime = datetime.strptime(opening, "%H:%M")
        # closingTime = datetime.strptime(closing, "%H:%M")

        # openingTime = str(openingTime)
        # closingTime = str(closingTime)


    else :

        db = sqlite3.connect('database.db')

        selectedDate = request.args.get('date')
        print("type(selectedDate)")
        print(type(selectedDate))
        print("selectedDate")
        print(selectedDate)

        if selectedDate == None:
            selectedDate = datetime.today().strftime('%d-%m-%Y')
        else:
            selectedDate = datetime. strptime(selectedDate, '%Y-%m-%d')
            selectedDate = datetime.strftime(selectedDate, '%d-%m-%Y')

        nextDay = datetime.strptime(selectedDate, '%d-%m-%Y') + timedelta(days=1)
        nextDay = datetime.strftime(nextDay, '%d-%m-%Y')

        # print(type(selectedDate))
        # print(type(datetime.strptime(selectedDate, '%d-%m-%Y')))
        
        print("selectedDate")
        print(selectedDate)
        print("nextDay")
        print(nextDay)
        # print(type(nextDay))
        # print("nextDay")
        # print(nextDay)

        try:
        
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            cur.execute("SELECT * FROM venues CROSS JOIN venue_type ON venues.venue_type = venue_type.type_id ")

            venues = cur.fetchall()

            cur.execute("SELECT * FROM venue_type")
            venue_type = cur.fetchall()

            cur.execute("SELECT * FROM config")
            config = cur.fetchall()

            cur.execute("SELECT * FROM orders WHERE start_date > '" + str(selectedDate) + "' AND end_date < '" + str(nextDay) + "'"  )
            orders = cur.fetchall()

        except sqlite3.Error as er:
            print(er)


        return render_template("member/book.html", venues=venues, venue_type=venue_type, config=config, orders=orders )

@book_member.route("/member/book/order", methods=["POST"])
@member_login_required
def book_order():

    formDate = request.form.get("form-date")
    formTime = request.form.get("form-time")
    formHours = request.form.get("form-hours")
    venue_id = request.form.get("venue_id")
    user_id = session["user_id"]
    price = ""
    
    print("xxxxxxx")
    print(session["user_id"])
    print(formDate)
    print(formTime)
    print(formHours)
    print(venue_id)

    db = sqlite3.connect('database.db')

    try:

        hour = int(formTime.split(":")[0])
        hour += int(formHours)
        if hour < 10 :
            hour = "0" + str(hour)
        else:
            hour = str(hour)

        print(hour)

        start_date = formDate + " " + formTime
        end_date = formDate + " " + hour + ":00"

        print(start_date)
        print(end_date)

        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT priceperhour FROM venues WHERE venue_id = '" + venue_id + "'")

        row = cur.fetchone()

        print(row[0])
        price = row[0]
        
        db.execute('INSERT INTO orders (venue_id, start_date, end_date, user_id, price, payment_method) VALUES (?,?,?,?,?,?) ' ,(venue_id, start_date, end_date, user_id, price, "cash") )
        db.commit()
        db.close()

        return redirect("/member/book?status=1&msg=Booked successfully, go to <a href='/member/history'>History</a> to view details")
    except sqlite3.Error as er:
        print(er)
        return redirect("/member/book?status=2&msg=Error! ")

@book_member.after_request
def response_processor(response):
    after_request(response)
    return response

# @login_member.before_request
# def beforerequest():
#     before_request()