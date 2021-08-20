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

@app.route('/details/transaction/<int:id>', methods=['GET', 'POST'])
@login_required
def transactionDetails(id):
    try:
        trans = transactionTable.query.filter(transactionTable.userid == current_user.id). filter(transactionTable.transactionid == id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        trans = transactionTable.query.filter(transactionTable.userid == current_user.id). filter(transactionTable.transactionid == id).first()

    if trans:
        customername = trans.transactionsource

        try:
            customer = customerTable.query.filter(customerTable.userid == current_user.id). filter(customerTable.customername == customername).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customer = customerTable.query.filter(customerTable.userid == current_user.id). filter(customerTable.customername == customername).first()

    return render_template('/details/transaction.html', trans = trans, customer=customer)

@app.route('/details/payable/<int:id>', methods=['GET', 'POST'])
@login_required
def payDetails(id):
    try:
        trans = accountsPayableTable.query.filter(accountsPayableTable.userid == current_user.id). filter(accountsPayableTable.transactionid == id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        trans = accountsPayableTable.query.filter(accountsPayableTable.userid == current_user.id). filter(accountsPayableTable.transactionid == id).first()

    return render_template('/details/payable.html', trans = trans)

@app.route('/details/receivable/<int:id>', methods=['GET', 'POST'])
@login_required
def recDetails(id):
    try:
        trans = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id). filter(accountsReceivableTable.transactionid == id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        trans = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id). filter(accountsReceivableTable.transactionid == id).first()

    if trans:
        customername = trans.transactionsource

        try:
            customer = customerTable.query.filter(customerTable.userid == current_user.id). filter(customerTable.customername == customername).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customer = customerTable.query.filter(customerTable.userid == current_user.id). filter(customerTable.customername == customername).first()

    return render_template('/details/receivable.html', trans = trans, customer=customer)

@app.route('/details/customer/<int:id>', methods=['GET', 'POST'])
@login_required
def customerDetails(id):
    try:
        cust = customerTable.query.filter(customerTable.userid == current_user.id). filter(customerTable.customerid == id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        cust = customerTable.query.filter(customerTable.userid == current_user.id). filter(customerTable.customerid == id).first()

    return render_template('/details/customer.html', customer=cust)