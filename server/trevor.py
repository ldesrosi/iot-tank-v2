# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

"""

import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

@app.route('/')
def show_dashboard():
    return render_template('dashboard.html')
