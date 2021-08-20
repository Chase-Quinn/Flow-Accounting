import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import *
from flow.models import *
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import *
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import *
import calendar

@app.route('/feedback', methods=['GET'])
@login_required
def feedback():
    form = FeedbackForm()

    return render_template('feedback.html', form=form)

@app.route('/feedback/bug-report', methods=['GET'])
@login_required
def bugReport():
    form = BugReportForm()

    return render_template('feedback/bug-report.html', form=form)