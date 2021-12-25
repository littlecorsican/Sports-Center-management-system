from flask import Flask, flash, redirect, render_template, request, session, copy_current_request_context
from flask import Blueprint

#app = Flask(__name__)

gallery_member = Blueprint('gallery_member', __name__)

from helpers import member_login_required, before_request, after_request


@gallery_member.route("/member/gallery", methods=["GET"])
@member_login_required
def gallery():

    return render_template("member/gallery.html")


@gallery_member.after_request
def response_processor(response):
    after_request(response)
    return response

# @dashboard_member.before_request
# def beforerequest():
#     before_request()