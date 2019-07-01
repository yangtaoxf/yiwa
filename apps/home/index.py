# coding: utf8

from apps import app
from flask import render_template


@app.route('/home')
def home():
    return render_template("home/home.html")
