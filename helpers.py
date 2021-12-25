import os
import requests
import urllib.parse
import re

from flask import redirect, render_template, request, session
from functools import wraps


os.environ['salt'] = 'sdaf2346dsf1234sdar34'

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def admin_login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("user_type") != "admin":
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return decorated_function

def member_login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("user_type") != "member":
            return redirect("/member/login")
        return f(*args, **kwargs)
    return decorated_function

def listToString(s): 
    
    str1 = "" 
    
    for ele in s: 
        str1 += " " + ele  
    
    return str1 

def sqlLiteRowToDict(rows): 

    arr = []


    for row in rows:
        rowDict = {}
        n = 0 
        for key in row.keys():
            for index, value in enumerate(row):
                if n == index:
                    print(key)
                    print(value)
                    rowDict[key] = value
            n += 1
        arr.append(rowDict)

    return {"dict" : arr}


def isTimeFormat(str):

    if ":" not in str: 
        return False
    
    if re.search('[a-zA-Z]', str) :
        return False

    splitStr = str.split(":")
    try:
        hours = int(splitStr[0])
        mins = int(splitStr[1])
        if hours > 24 :
            return False
        if mins > 59 or mins < 0 :
            return False
    except:
        return False

    return True



def before_request():

    print('endpoint: %s, url: %s, path: %s' % (
        request.endpoint,
        request.url,
        request.path))

    #not in used anymore
    # pathSplit = request.path[1:].split("/")

    # print(pathSplit)
    # print(len(pathSplit))

    # if len(pathSplit) > 1 :

    #     user = pathSplit[0]
    #     print("user")
    #     print(user)

    #     page = pathSplit[1]
    #     print("page")
    #     print(page)

    #     checkIfRequestIsFile = pathSplit[len(pathSplit)-1]
    #     if "." not in checkIfRequestIsFile: 


    #         mod = __import__("controllers." + user, fromlist=[page])
    #         klass = getattr(mod, page)
    #         getattr(klass, page)()

def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

