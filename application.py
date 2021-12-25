import os


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
#import hashlib
#application.app.folder.file
from routes.admin.dashboard import dashboard_admin
from routes.admin.login import login_admin
from routes.admin.register import register_admin
from routes.admin.orders import order_admin
from routes.admin.approve import approve_admin
from routes.admin.setting import setting_admin
from routes.admin.search import search_admin

from routes.member.dashboard import dashboard_member
from routes.member.login import login_member
from routes.member.register import register_member
from routes.member.gallery import gallery_member
from routes.member.about import about_member
from routes.member.history import history_member
from routes.member.book import book_member

from helpers import apology

# Configure application
app = Flask(__name__, static_url_path='/static')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.register_blueprint(dashboard_admin)
app.register_blueprint(login_admin)
app.register_blueprint(register_admin)
app.register_blueprint(order_admin)
app.register_blueprint(approve_admin)
app.register_blueprint(setting_admin)
app.register_blueprint(search_admin)
app.register_blueprint(dashboard_member)
app.register_blueprint(login_member)
app.register_blueprint(register_member)
app.register_blueprint(gallery_member)
app.register_blueprint(about_member)
app.register_blueprint(book_member)
app.register_blueprint(history_member)

# directory = "routes/admin/"

# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     if os.path.isfile(f):
#         print(f)
#         print(filename)



# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
#db = sqlite3.connect("database.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/")
def index():

    rows = []
    config = []

    db = sqlite3.connect('database.db')

    try:
        
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT venue_type.Type, COUNT(venues.venue_id) FROM venues CROSS JOIN venue_type ON venues.venue_type = venue_type.type_id GROUP BY venue_type.Type")

        rows = cur.fetchall()

        cur.execute("SELECT * FROM config")
        config = cur.fetchall()

    except sqlite3.Error as er:
        print(er)


    return render_template("index.html",rows=rows, config=config)

@app.route("/admin")
def admin():
    return redirect("/admin/dashboard")

@app.route("/member")
def member():
    return redirect("/member/dashboard")




@app.route("/login", methods=["GET", "POST"])
def login():

    return redirect("/member/login")


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    return redirect("/member/register")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == "__main__":
    app.run()
    