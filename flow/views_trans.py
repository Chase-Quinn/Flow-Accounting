import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import SignupForm, LoginForm, AccountForm, UpdateAccountForm, VendorForm, CustomerForm, InvestmentForm, TransactionIncomeForm, TransactionExpenseForm, DebtForm, FeedbackForm, BugReportForm, TransactionFormRange, TransactionModifyForm, TransactionDeleteForm, CustomerModifyForm, VendorModifyForm, DebtDeleteForm
from flow.models import *
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import AccountResults, TransactionResults, CustomerResults, DebtResults, VendorResults
from flow.sorting import sort7day, sortmonth, sortthreemonth, sortsixmonth, sortyear, sortthreeyear, sortfiveyear, addTotals
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import *
import calendar

@app.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    try:
        transactions = transactionTable.query.filter_by(userid=current_user.id).order_by(desc(transactionTable.transactiondate)).limit(250).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        transactions = transactionTable.query.filter_by(userid=current_user.id).order_by(desc(transactionTable.transactiondate)).limit(250).all()
    add2 = Decimal(10) ** -2

    form1 = TransactionFormRange()
    form2 = TransactionDeleteForm()
    form3 = TransactionModifyForm()

    if form1.validate_on_submit():
        return redirect(url_for('transactionsAdjusted'))

    if form2.validate_on_submit():
        transactionnumber2 = form2.transactionnumber2.data
        try:
            transactiontest = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            transactiontest = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).first()
        if transactiontest:
            try:
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            if transactiontest.transactiontype == 'Income' or transactiontest.transactiontype == 'Investment':
                bank.bankbalance -= transactiontest.totalamount
                try:
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance -= transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance -= transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
            if transactiontest.transactiontype == 'Expense':
                bank.bankbalance += transactiontest.totalamount
                try:
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance += transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance += transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
            try:
                transactiondelete = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).delete()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                transactiondelete = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).delete()
                db.session.commit()
            flash(f'Transaction Deleted!', 'success')
            return redirect(url_for('transactions'))
        else:
            flash(f'Error: Check your information', 'error')
            return redirect(url_for('transactions'))

    if form3.validate_on_submit():
        transactionnumber3 = form3.transactionnumber3.data
        transactionamount = form3.transactionamount.data
        transactiondescription = form3.transactiondescription.data
        transactionmethod = form3.transactionmethod.data
        transactiondate = form3.transactiondate.data

        try:
            transactiontest2 = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            transactiontest2 = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
        if transactiontest2:
            try:
                transaction = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                transaction = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
            transaction.accountid = accountnumber
            transaction.totalamount = transactionamount
            transaction.transactiondescription = transactiondescription
            db.session.flush()
            db.session.commit()
            transaction.transactionmethod = transactionmethod
            transaction.transactiondate = transactiondate
            transaction.transactionreason = transactionreason
            db.session.flush()
            db.session.commit()

            flash(f'Transaction Modified!', 'success')
            return redirect(url_for('transactions'))
        else:
            flash(f'Error: Check your information', 'error')
            return redirect(url_for('transactions'))
    
    for transaction in transactions:
        new = Decimal(transaction.totalamount).quantize(add2)
        transaction.totalamount = "{:,}".format(new)

    return render_template('transactions.html', rows = transactions, form1=form1, form2=form2, form3=form3)

@app.route('/transactions-adjusted', methods=['GET'])
@login_required
def transactionsAdjusted():
    # we are going to pass the form data to this, query between the two dates that are given
    range1 = request.args.get('rangestart')
    range2 = request.args.get('rangeend')
    try:
        transactions = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= range1).\
            filter(transactionTable.transactiondate <= range2).order_by(desc(transactionTable.transactiondate))
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        transactions = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= range1).\
            filter(transactionTable.transactiondate <= range2).order_by(desc(transactionTable.transactiondate))

    add2 = Decimal(10) ** -2
    
    form1 = TransactionFormRange()
    form2 = TransactionDeleteForm()
    form3 = TransactionModifyForm()

    if form1.validate_on_submit():
        return redirect(url_for('transactionsAdjusted'))

    if form2.validate_on_submit():
        transactionnumber2 = form2.transactionnumber2.data
        try:
            transactiontest = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            transactiontest = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).first()
        if transactiontest:
            try:
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            if transactiontest.transactiontype == 'Income' or transactiontest.transactiontype == 'Investment':
                try:
                    bank.bankbalance -= transactiontest.totalamount
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance -= transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bank.bankbalance -= transactiontest.totalamount
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance -= transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
            if transactiontest.transactiontype == 'Expense':
                try:
                    bank.bankbalance += transactiontest.totalamount
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance += transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bank.bankbalance += transactiontest.totalamount
                    balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transactiontest.transactiondate).all()
                    for bal in balance:
                        bal.bankbalance += transactiontest.totalamount
                    db.session.flush()
                    db.session.commit()
            try:
                transactiondelete = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).delete()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                transactiondelete = transactionTable.query.filter(transactionTable.transactionid == transactionnumber2).filter(transactionTable.userid == current_user.id).delete()
                db.session.commit()
            flash(f'Transaction Deleted!', 'success')
            return redirect(url_for('transactionsAdjusted'))
        else:
            flash(f'Error: Check your information', 'error')
            return redirect(url_for('transactionsAdjusted'))

    if form3.validate_on_submit():
        transactionnumber3 = form3.transactionnumber3.data
        accountnumber = form3.accountnumber.data
        transactionamount = form3.transactionamount.data
        transactiondescription = form3.transactiondescription.data
        transactionmethod = form3.transactionmethod.data
        transactiondate = form3.transactiondate.data
        transactionreason = form3.transactionreason.data

        try:
            transactiontest2 = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            transactiontest2 = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
        if transactiontest2:
            try:
                transaction = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                transaction = transactionTable.query.filter(transactionTable.transactionid == transactionnumber3).filter(transactionTable.userid == current_user.id).first()
            transaction.accountid = accountnumber
            transaction.totalamount = transactionamount
            transaction.transactiondescription = transactiondescription
            db.session.flush()
            db.session.commit()
            transaction.transactionmethod = transactionmethod
            transaction.transactiondate = transactiondate
            transaction.transactionreason = transactionreason
            db.session.flush()
            db.session.commit()

            flash(f'Transaction Modified!', 'success')
            return redirect(url_for('transactionsAdjusted'))
        else:
            flash(f'Error: Check your information', 'error')
            return redirect(url_for('transactionsAdjusted'))

    for transaction in transactions:
        new = Decimal(transaction.totalamount).quantize(add2)
        transaction.totalamount = "{:,}".format(new)
        
    return render_template('transactions-adjusted.html', rows = transactions, rangestart = range1, rangeend=range2, form1=form1, form2=form2, form3=form3)