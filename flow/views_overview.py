import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import *
from flow.models import *
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import AccountResults, TransactionResults, CustomerResults, DebtResults, VendorResults
from flow.sorting import sort7day, sortmonth, sortthreemonth, sortsixmonth, sortyear, sortthreeyear, sortfiveyear, addTotals, addOther
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import *
import calendar

@app.route('/overview', methods=['GET'])
@login_required
def overview():
    def findbalance(userid):
        try:
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        return '{}'.format(balance.bankbalance)
    
    def findbank(userid):
        try:
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        return '{}'.format(balance.bankname)

    sevendaysago = (date.today() - timedelta(days = 6))
    monthago = (date.today() - timedelta(days = 30))
    threemonthsago = date.today() - relativedelta(months = 3)
    sixmonthsago = date.today() - relativedelta(months = 6)
    yearago = date.today() - relativedelta(years = 1)
    threeyearsago = date.today() - relativedelta(years = 3)
    fiveyearsago = date.today() - relativedelta(years = 5)

    userquery = usersTable.query.filter(usersTable.id == current_user.id).first()
    fiscalstart = userquery.fiscalyearstart
    fiscalend = userquery.fiscalyearend

    try:
        income7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Income').all()
        expense7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Expense').all()
        incomemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Income').all()
        expensemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomesixmonthquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensesixmonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Income').all()
        expenseyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreeyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomefiveyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensefiveyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Expense').all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        income7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Income').all()
        expense7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Expense').all()
        incomemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Income').all()
        expensemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomesixmonthquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensesixmonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Income').all()
        expenseyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreeyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomefiveyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensefiveyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Expense').all()

    sevendayincomedata = sort7day(income7dayquery)
    sevendayexpensedata = sort7day(expense7dayquery)
    monthincomedata = sortmonth(incomemonthquery)
    monthexpensedata = sortmonth(expensemonthquery)
    threemonthincomedata = sortthreemonth(incomethreemonthquery)
    threemonthexpensedata = sortthreemonth(expensethreemonthquery)
    sixmonthincomedata = sortsixmonth(incomesixmonthquery)
    sixmonthexpensedata = sortsixmonth(expensesixmonthquery)
    yearincomedata = sortyear(incomeyearquery)
    yearexpensedata = sortyear(expenseyearquery)
    threeyearincomedata = sortthreeyear(incomethreeyearquery)
    threeyearexpensedata = sortthreeyear(expensethreeyearquery)
    fiveyearincomedata = sortfiveyear(incomefiveyearquery)
    fiveyearexpensedata = sortfiveyear(expensefiveyearquery)

    try:
        payrollexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Payroll').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        utilitiesexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Utilities').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        advertisementsexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Advertisements').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        salesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Sales').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        servicesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Services').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Other Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        revenue = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        payrollexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Payroll').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        utilitiesexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Utilities').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        advertisementsexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Advertisements').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        salesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Sales').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        servicesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Services').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Other Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        revenue = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()

    payrolltotal = addTotals(payrollexpense)
    utilitiestotal = addTotals(utilitiesexpense)
    advertisementstotal = addTotals(advertisementsexpense)
    otherexpensetotal = addOther(otherexpense)
    salestotal = addTotals(salesincome)
    servicestotal = addTotals(servicesincome)
    otherincometotal = addTotals(otherincome)
    revenuetotal = addTotals(revenue)
    expense = payrolltotal + utilitiestotal + advertisementstotal + otherexpensetotal

    add2 = Decimal(10) ** -2

    expensestats = [Decimal(payrolltotal).quantize(add2), Decimal(utilitiestotal).quantize(add2), Decimal(advertisementstotal).quantize(add2), Decimal(otherexpensetotal).quantize(add2)]
    incomestats = [Decimal(salestotal).quantize(add2), Decimal(servicestotal).quantize(add2), Decimal(otherincometotal).quantize(add2), Decimal(revenuetotal).quantize(add2)]

    totalexpenses = payrolltotal + utilitiestotal + advertisementstotal + otherexpensetotal
    totalincome = salestotal + servicestotal + otherincometotal

    balance = findbalance(current_user.id)
    bankbalance = Decimal(balance).quantize(add2)
    bankname = findbank(current_user.id)
    totalexpense = Decimal(expense).quantize(add2)

    def pastduepayables(userid):
        try:
            pay = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate < date.today()).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            pay = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate < date.today()).all()
        due = 0
        for pays in pay:
            due += 1
        return due

    def pastduereceivables(userid):
        try:
            rec = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.duedate < date.today()).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            rec = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.duedate < date.today()).all()
        due = 0
        for recs in rec:
            due += 1
        return due

    payablesdue = pastduepayables(current_user.id)
    receivablesdue = pastduereceivables(current_user.id)

    try:
        totmem = usersTable.query.filter(usersTable.member == True).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        totmem = usersTable.query.filter(usersTable.member == True).all()
    def addmems():
        mems = 0
        for mem in totmem:
            mems += 1
        return mems
    members = addmems()

    return render_template('overview.html', sevendayincomedata=sevendayincomedata, sevendayexpensedata = sevendayexpensedata, monthincomedata=monthincomedata, monthexpensedata = monthexpensedata,
                            threemonthincomedata=threemonthincomedata, threemonthexpensedata = threemonthexpensedata, sixmonthincomedata=sixmonthincomedata, sixmonthexpensedata = sixmonthexpensedata,
                            yearincomedata=yearincomedata, yearexpensedata = yearexpensedata, threeyearincomedata=threeyearincomedata, threeyearexpensedata = threeyearexpensedata,
                            fiveyearincomedata=fiveyearincomedata, fiveyearexpensedata = fiveyearexpensedata, payroll = "{:,}".format(expensestats[0]), utilities = "{:,}".format(expensestats[1]), advertisements = "{:,}".format(expensestats[2]),
                            otherexpense = "{:,}".format(expensestats[3]), sales = "{:,}".format(incomestats[0]), services = "{:,}".format(incomestats[1]), otherincome = "{:,}".format(incomestats[2]), otherincometotal = Decimal(otherincometotal).quantize(add2), revenue = "{:,}".format(incomestats[3]), fiscalstart = fiscalstart,
                            fiscalend = fiscalend, totalexpenses = totalexpenses, totalincome = totalincome, salestotal = Decimal(salestotal).quantize(add2), servicestotal = Decimal(servicestotal).quantize(add2),
                            otherexpensetotal = Decimal(otherexpensetotal).quantize(add2), advertisementstotal = Decimal(advertisementstotal).quantize(add2), utilitiestotal = Decimal(utilitiestotal).quantize(add2),
                            payrolltotal = Decimal(payrolltotal).quantize(add2), balance = "{:,}".format(bankbalance), bankname = bankname, payablesdue = payablesdue, receivablesdue = receivablesdue, totalexpensesstat = "{:,}".format(totalexpense), members = members)



@app.route('/mobile/overview', methods=['GET'])
@login_required
def mobileOverview():
    def findbalance(userid):
        try:
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        return '{}'.format(balance.bankbalance)
    
    def findbank(userid):
        try:
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        return '{}'.format(balance.bankname)

    sevendaysago = (date.today() - timedelta(days = 6))
    monthago = (date.today() - timedelta(days = 30))
    threemonthsago = date.today() - relativedelta(months = 3)
    sixmonthsago = date.today() - relativedelta(months = 6)
    yearago = date.today() - relativedelta(years = 1)
    threeyearsago = date.today() - relativedelta(years = 3)
    fiveyearsago = date.today() - relativedelta(years = 5)

    userquery = usersTable.query.filter(usersTable.id == current_user.id).first()
    fiscalstart = userquery.fiscalyearstart
    fiscalend = userquery.fiscalyearend

    try:
        income7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Income').all()
        expense7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Expense').all()
        incomemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Income').all()
        expensemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomesixmonthquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensesixmonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Income').all()
        expenseyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreeyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomefiveyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensefiveyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Expense').all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        income7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Income').all()
        expense7dayquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sevendaysago).filter(transactionTable.transactiontype == 'Expense').all()
        incomemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Income').all()
        expensemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= monthago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreemonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threemonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomesixmonthquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Income').all()
        expensesixmonthquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= sixmonthsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Income').all()
        expenseyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= yearago).filter(transactionTable.transactiontype == 'Expense').all()
        incomethreeyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensethreeyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= threeyearsago).filter(transactionTable.transactiontype == 'Expense').all()
        incomefiveyearquery= transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Income').all()
        expensefiveyearquery = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate <= date.today()).filter(transactionTable.transactiondate >= fiveyearsago).filter(transactionTable.transactiontype == 'Expense').all()

    sevendayincomedata = sort7day(income7dayquery)
    sevendayexpensedata = sort7day(expense7dayquery)
    monthincomedata = sortmonth(incomemonthquery)
    monthexpensedata = sortmonth(expensemonthquery)
    threemonthincomedata = sortthreemonth(incomethreemonthquery)
    threemonthexpensedata = sortthreemonth(expensethreemonthquery)
    sixmonthincomedata = sortsixmonth(incomesixmonthquery)
    sixmonthexpensedata = sortsixmonth(expensesixmonthquery)
    yearincomedata = sortyear(incomeyearquery)
    yearexpensedata = sortyear(expenseyearquery)
    threeyearincomedata = sortthreeyear(incomethreeyearquery)
    threeyearexpensedata = sortthreeyear(expensethreeyearquery)
    fiveyearincomedata = sortfiveyear(incomefiveyearquery)
    fiveyearexpensedata = sortfiveyear(expensefiveyearquery)

    try:
        payrollexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Payroll').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        utilitiesexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Utilities').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        advertisementsexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Advertisements').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        salesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Sales').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        servicesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Services').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Other Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        revenue = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        payrollexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Payroll').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        utilitiesexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Utilities').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        advertisementsexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactionreason == 'Advertisements').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherexpense = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Expense').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        salesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Sales').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        servicesincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Services').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        otherincome = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactionreason == 'Other Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()
        revenue = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= fiscalstart).filter(transactionTable.transactiondate <= fiscalend).all()

    payrolltotal = addTotals(payrollexpense)
    utilitiestotal = addTotals(utilitiesexpense)
    advertisementstotal = addTotals(advertisementsexpense)
    otherexpensetotal = addOther(otherexpense)
    salestotal = addTotals(salesincome)
    servicestotal = addTotals(servicesincome)
    otherincometotal = addTotals(otherincome)
    revenuetotal = addTotals(revenue)
    expense = payrolltotal + utilitiestotal + advertisementstotal + otherexpensetotal

    add2 = Decimal(10) ** -2

    expensestats = [Decimal(payrolltotal).quantize(add2), Decimal(utilitiestotal).quantize(add2), Decimal(advertisementstotal).quantize(add2), Decimal(otherexpensetotal).quantize(add2)]
    incomestats = [Decimal(salestotal).quantize(add2), Decimal(servicestotal).quantize(add2), Decimal(otherincometotal).quantize(add2), Decimal(revenuetotal).quantize(add2)]

    totalexpenses = payrolltotal + utilitiestotal + advertisementstotal + otherexpensetotal
    totalincome = salestotal + servicestotal + otherincometotal

    balance = findbalance(current_user.id)
    bankbalance = Decimal(balance).quantize(add2)
    bankname = findbank(current_user.id)
    totalexpense = Decimal(expense).quantize(add2)

    def pastduepayables(userid):
        try:
            pay = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate < date.today()).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            pay = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate < date.today()).all()
        due = 0
        for pays in pay:
            due += 1
        return due

    def pastduereceivables(userid):
        try:
            rec = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.duedate < date.today()).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            rec = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.duedate < date.today()).all()
        due = 0
        for recs in rec:
            due += 1
        return due

    payablesdue = pastduepayables(current_user.id)
    receivablesdue = pastduereceivables(current_user.id)

    try:
        totmem = usersTable.query.filter(usersTable.member == True).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        totmem = usersTable.query.filter(usersTable.member == True).all()
    def addmems():
        mems = 0
        for mem in totmem:
            mems += 1
        return mems
    members = addmems()
    return render_template('/mobile/overview.html', sevendayincomedata=sevendayincomedata, sevendayexpensedata = sevendayexpensedata, monthincomedata=monthincomedata, monthexpensedata = monthexpensedata,
                            threemonthincomedata=threemonthincomedata, threemonthexpensedata = threemonthexpensedata, sixmonthincomedata=sixmonthincomedata, sixmonthexpensedata = sixmonthexpensedata,
                            yearincomedata=yearincomedata, yearexpensedata = yearexpensedata, threeyearincomedata=threeyearincomedata, threeyearexpensedata = threeyearexpensedata,
                            fiveyearincomedata=fiveyearincomedata, fiveyearexpensedata = fiveyearexpensedata, payroll = "{:,}".format(expensestats[0]), utilities = "{:,}".format(expensestats[1]), advertisements = "{:,}".format(expensestats[2]),
                            otherexpense = "{:,}".format(expensestats[3]), sales = "{:,}".format(incomestats[0]), services = "{:,}".format(incomestats[1]), otherincome = "{:,}".format(incomestats[2]), otherincometotal = Decimal(otherincometotal).quantize(add2), revenue = "{:,}".format(incomestats[3]), fiscalstart = fiscalstart,
                            fiscalend = fiscalend, totalexpenses = totalexpenses, totalincome = totalincome, salestotal = Decimal(salestotal).quantize(add2), servicestotal = Decimal(servicestotal).quantize(add2),
                            otherexpensetotal = Decimal(otherexpensetotal).quantize(add2), advertisementstotal = Decimal(advertisementstotal).quantize(add2), utilitiestotal = Decimal(utilitiestotal).quantize(add2),
                            payrolltotal = Decimal(payrolltotal).quantize(add2), balance = "{:,}".format(bankbalance), bankname = bankname, payablesdue = payablesdue, receivablesdue = receivablesdue, totalexpensesstat = "{:,}".format(totalexpense), members = members)