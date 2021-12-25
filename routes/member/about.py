from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint

#app = Flask(__name__)

about_member = Blueprint('about_member', __name__)

from helpers import member_login_required, before_request, after_request


@about_member.route("/member/about", methods=["GET"])
def gallery():

    return render_template("member/about.html")


@about_member.after_request
def response_processor(response):
    after_request(response)
    return response

# @dashboard_member.before_request
# def beforerequest():
#     before_request()