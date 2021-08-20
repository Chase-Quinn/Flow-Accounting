import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import *
from flow.models import usersTable, subuserTable, accountTable, transactionTable, investmentTable, debtTable, customerTable, vendorTable
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import AccountResults, TransactionResults, CustomerResults, DebtResults, VendorResults
from flow.sorting import sort7day, sortmonth, sortthreemonth, sortsixmonth, sortyear, sortthreeyear, sortfiveyear, addTotals
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar

@app.route('/Account-Chart', methods=['GET', 'POST'])
@login_required
def accountChart():
    try:
        accounts = accountTable.query.filter(accountTable.userid==current_user.id).filter_by(main=True).order_by(asc(accountTable.accountnumber))
        table = AccountResults(accounts)
        form = AccountModify()

        if form.validate_on_submit():
            accounttest = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.accountnumber == form.accountnumber.data).first()
            if not accounttest:
                flash(f'There was an error, please check your information.', 'error')
                return redirect(url_for('accountChart'))
            elif accounttest.main == True:
                accounttest.accountnumber = form.accountnumber.data
                accounttest.accountname = form.accountname.data
                accounttest.accountdescription = form.accountdescription.data
                accounttest.accountdate = form.accountdate.data
                db.session.commit()
                flash(f'Account Modified!', 'success')
                return redirect(url_for('accountChart'))
            elif accounttest.main == False:
                flash(f'You can only modify main accounts, please go to views -> accounts to delete a sub-account.', 'error')
                return redirect(url_for('accountChart'))
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        accounts = accountTable.query.filter(accountTable.userid==current_user.id).filter_by(main=True).order_by(asc(accountTable.accountnumber))
        table = AccountResults(accounts)
        form = AccountModify()

        if form.validate_on_submit():
            accounttest = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.accountnumber == form.accountnumber.data).first()
            if not accounttest:
                flash(f'There was an error, please check your information.', 'error')
                return redirect(url_for('accountChart'))
            elif accounttest.main == True:
                accounttest.accountnumber = form.accountnumber.data
                accounttest.accountname = form.accountname.data
                accounttest.accountdescription = form.accountdescription.data
                accounttest.accountdate = form.accountdate.data
                db.session.commit()
                flash(f'Account Modified!', 'success')
                return redirect(url_for('accountChart'))
            elif accounttest.main == False:
                flash(f'You can only modify main accounts, please go to views -> accounts to delete a sub-account.', 'error')
                return redirect(url_for('accountChart'))

    return render_template('Account-Chart.html', table=table, form=form)

@app.route('/view/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    try:
        accounts = accountTable.query.filter(accountTable.userid==current_user.id).order_by(asc(accountTable.accountnumber))
        form1 = AccountDelete()

        if form1.validate_on_submit():
            accounttest = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.accountnumber == form1.accountnumber1.data).first()
            if not accounttest:
                flash(f'There was an error, please check your information.', 'error')
                return redirect(url_for('accounts'))
            if accounttest.main == True:
                flash(f'You can not delete a main account number, please modify it within the Chart of Accounts.', 'error')
                return redirect(url_for('accounts'))
            if accounttest.main == False:
                accountdelete = accountTable.query.filter(accountTable.accountnumber == form1.accountnumber1.data).filter(accountTable.userid == current_user.id).delete()
                db.session.commit()
                flash(f'Account Deleted!', 'success')
                return redirect(url_for('accounts'))
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        accounts = accountTable.query.filter(accountTable.userid==current_user.id).order_by(asc(accountTable.accountnumber))
        form1 = AccountDelete()

        if form1.validate_on_submit():
            accounttest = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.accountnumber == form1.accountnumber1.data).first()
            if not accounttest:
                flash(f'There was an error, please check your information.', 'error')
                return redirect(url_for('accounts'))
            if accounttest.main == True:
                flash(f'You can not delete a main account number, please modify it within the Chart of Accounts.', 'error')
                return redirect(url_for('accounts'))
            if accounttest.main == False:
                accountdelete = accountTable.query.filter(accountTable.accountnumber == form1.accountnumber1.data).filter(accountTable.userid == current_user.id).delete()
                db.session.commit()
                flash(f'Account Deleted!', 'success')
                return redirect(url_for('accounts'))

    return render_template('view/accounts.html', rows=accounts, form1=form1)