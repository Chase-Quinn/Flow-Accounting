import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import *
from flow.models import *
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import *
from flow.sorting import sort7day, sortmonth, sortthreemonth, sortsixmonth, sortyear, sortthreeyear, sortfiveyear, addTotals
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import *
import calendar

@app.route('/transaction/invoice/<int:id>', methods=['GET'])
@login_required
def invoice(id):
    if id:
        transid = id
    try:
        trans = transactionTable.query.filter(transactionTable.transactionid == transid).filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        trans = transactionTable.query.filter(transactionTable.transactionid == transid).filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').first()
    
    if trans:
        cust = trans.transactionsource
        # try:
        #     customer = customerTable.query.filter(customerTable.userid == current_user.id).filter(customerTable.customername == cust).first()
        # except(AttributeError, SQLAlchemy.exc.OperationalError):
        customer = customerTable.query.filter(customerTable.userid == current_user.id).filter(customerTable.customername == cust).first()

        ex = 'Hello'
    
    if not id:
        ex = 'No ID'


    return render_template('/invoice/invoice.html', customer = customer, trans = trans, ex=ex)