# coding: utf8

from apps import app
from flask import render_template
from yiwa.api import render_template_with_qrcode


@app.route('/home')
def home():
    # return render_template("home/home.html")
    return render_template_with_qrcode("home/home.html")
