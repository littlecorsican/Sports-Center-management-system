from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint
import sqlite3
import time
from datetime import datetime
import sys

#app = Flask(__name__)

setting_admin = Blueprint('setting_admin', __name__)

from helpers import admin_login_required, before_request, after_request, listToString, isTimeFormat


@setting_admin.route("/admin/setting", methods=["GET", "POST"])
@admin_login_required
def setting():

    if request.method == "POST":
        return ""

    else :

        db = sqlite3.connect('database.db')

        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM venues CROSS JOIN venue_type ON venues.venue_type = venue_type.type_id ORDER BY venues.venue_type")

        venues = cur.fetchall()


        cur.execute("SELECT * FROM venue_type ")

        venue_type = cur.fetchall()

        cur.execute("SELECT * FROM config ")

        config = cur.fetchall()
        
        return render_template("admin/setting.html", venues=venues , venue_type = venue_type, config=config)

@setting_admin.route("/admin/setting/add", methods=["POST"])
@admin_login_required
def setting_add():

    if request.method == "POST":
        
        vType = int(request.form.get("type"))
        name = request.form.get("name")
        priceperhour = request.form.get("priceperhour")

        db = sqlite3.connect('database.db')

        try:

            # cur = db.cursor()
            # cur.execute("SELECT Type FROM venue_type WHERE type_id = ? LIMIT 1", (vType,))

            # result = cur.fetchall()
            # typeStr = result[0]

            # print(typeStr[0])
            # print(type(typeStr[0]))
            
            db.execute('INSERT INTO venues (venue_type, reference_name, priceperhour) VALUES (?,?,?) ' ,(vType, name, priceperhour) )
            db.commit()
            db.close()

            return redirect("/admin/setting?status=1&msg=Added successfully")
        except sqlite3.Error as er:
            print(er)
            return redirect("/admin/setting?status=2&msg=Error! Fail to add")
        #return redirect("/admin/setting?status=2&msg=Error! Fail to add")

        

    else :

        return "invalid request"

@setting_admin.route("/admin/setting/addtype", methods=["POST"])
@admin_login_required
def setting_addtype():

    if request.method == "POST":

        venuetype = request.form.get("venuetype")
        print(venuetype)

        db = sqlite3.connect('database.db')

        try:
            
            db.execute('INSERT INTO venue_type (Type) VALUES (?) ' ,(venuetype,) )
            db.commit()
            db.close()

            return redirect("/admin/setting?status=1&msg=Added successfully")
        except sqlite3.Error as er:
            print(er)
            return redirect("/admin/setting?status=2&msg=Error! Fail to add")


    else :

        return "invalid request"

@setting_admin.route("/admin/setting/onmaintenance", methods=["POST"])
@admin_login_required
def setting_onmaintenance():

    if request.method == "POST":

        id = request.form.get("id")
        action = request.form.get("action")
        print(id)

        db = sqlite3.connect('database.db')

        try:
            
            db.execute("UPDATE venues SET under_maintenance = ? WHERE venue_id = ?" ,(action, id) )
            db.commit()
            db.close()

            return "Updated successfully"
        except sqlite3.Error as er:
            print(er)
            return "Fail to update"


    else :

        return "invalid request"


@setting_admin.route("/admin/setting/deleteVenue", methods=["POST"])
@admin_login_required
def setting_deleteVenue():

    if request.method == "POST":

        id = request.form.get("id")
        print(id)

        db = sqlite3.connect('database.db')

        try:
            
            db.execute('DELETE FROM venues WHERE venue_id=?' ,(id,) )
            db.commit()
            db.close()

            return "success"
        except sqlite3.Error as er:
            print(er)
            return "Fail to update"


    else :

        return "invalid request"

@setting_admin.route("/admin/setting/deleteVenueType", methods=["POST"])
@admin_login_required
def setting_deleteVenueType():

    if request.method == "POST":

        id = request.form.get("id")
        print(id)

        db = sqlite3.connect('database.db')

        try:
            
            db.execute('DELETE FROM venue_type WHERE type_id=?' ,(id,) )
            db.commit()
            db.close()

            return "success"
        except sqlite3.Error as er:
            print(er)
            return "Fail to update"


    else :

        return "invalid request"

@setting_admin.route("/admin/setting/setOffdays", methods=["POST"])
@admin_login_required
def setting_setOffdays():

    offdays = listToString(request.form.getlist("offdays"))

    print(offdays)

    db = sqlite3.connect('database.db')

    try:
        
        db.execute("UPDATE config SET value = ? WHERE key = ?" ,(offdays, "offdays") )
        db.commit()
        db.close()

        return redirect("/admin/setting?status=1&msg=Updated successfully")
    except sqlite3.Error as er:
        print(er)
        return redirect("/admin/setting?status=2&msg=Error! Fail to update")


@setting_admin.route("/admin/setting/set", methods=["POST"])
@admin_login_required
def setting_set():

    key = request.form.get("key")
    newValue = request.form.get("newValue")
    db = sqlite3.connect('database.db')

    if isTimeFormat(newValue) == False and (key == "daily_start" or key == "daily_end") :
        return "Fail to update"


    try:
        
        db.execute("UPDATE config SET value = ? WHERE key = ?" ,(newValue, key) )
        db.commit()
        db.close()

        return "success"
    except sqlite3.Error as er:
        print(er)
        return "Fail to update"

@setting_admin.after_request
def response_processor(response):
    after_request(response)
    return response

# @setting_admin.before_request
# def beforerequest():
#     before_request()