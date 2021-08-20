import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import *
from flask_mail import Mail, Message
from flow.models import usersTable, subuserTable, accountTable, transactionTable, investmentTable, debtTable, customerTable, vendorTable
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import AccountResults, TransactionResults, CustomerResults, DebtResults, VendorResults
from flow.sorting import sort7day, sortmonth, sortthreemonth, sortsixmonth, sortyear, sortthreeyear, sortfiveyear, addTotals
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar
from flow.views_statements import *
from flow.views_trans import *
from flow.views_newentry import *
from flow.views_views import *
from flow.views_feedback import *
from flow.views_overview import *
from flow.views_accounthandling import *
from flow.views_accounts import *
from flow.invoicing import *
from flow.details import *

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    form2 = EmailListForm()

    if form.validate_on_submit():
        msg = Message('Home Page Contact Message From ' + form.name.data, recipients=['flow.accounting@myflowapp.com'])
        msg.html = '<h3>Contact Message</h3> <br> <h4>Email:' + form.email.data + '</h4><br><h4>Name:' + form.name.data + '</h4> <br> <p>' + form.message.data + '</p>'
        mail.send(msg)
        flash(f'Your Message has been sent!  Thank you for your interest in Flow - Accounting Simplified!', 'success')
        return redirect(url_for('index'))

    if form2.validate_on_submit():
        exists = emailList.query.filter(emailList.email == form2.email2.data).first()
        if exists:
            flash(f"That email is already on our mailing list!", "success")
            return redirect(url_for('index'))
        if not exists:
            new_sub = emailList(email = form2.email2.data)
            try:
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('index'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('index'))

    return render_template('index.html', form=form, form2=form2)

@app.route('/about', methods=['GET', 'POST'])
def about():
    form = ContactForm()
    form2 = EmailListForm()

    if form.validate_on_submit():
        msg = Message('Home Page Contact Message From ' + form.name.data, recipients=['crtechsolutions01@gmail.com'])
        msg.html = '<h3>Contact Message</h3> <br> <h4>Email:' + form.email.data + '</h4><br><h4>Name:' + form.name.data + '</h4> <br> <p>' + form.message.data + '</p>'
        mail.send(msg)
        flash(f'Your Message has been sent!  Thank you for your interest in Flow - Accounting Simplified!', 'success')
        return redirect(url_for('about'))

    if form2.validate_on_submit():
        exists = emailList.query.filter(emailList.email == form2.email2.data).first()
        if exists:
            flash(f"That email is already on our mailing list!", "success")
            return redirect(url_for('about'))
        if not exists:
            new_sub = emailList(email = form2.email2.data)
            try:
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('about'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('about'))

    return render_template('about.html', form=form, form2=form2)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    form2 = EmailListForm()
    form3 = ContactPageForm()

    if form.validate_on_submit():
        msg = Message('Home Page Contact Message From ' + form.name.data, recipients=['crtechsolutions01@gmail.com'])
        msg.html = '<h3>Contact Message</h3> <br> <h4>Email:' + form.email.data + '</h4><br><h4>Name:' + form.name.data + '</h4> <br> <p>' + form.message.data + '</p>'
        mail.send(msg)
        flash(f'Your Message has been sent!  Thank you for your interest in Flow - Accounting Simplified!', 'success')
        return redirect(url_for('contact'))

    if form2.validate_on_submit():
        exists = emailList.query.filter(emailList.email == form2.email2.data).first()
        if exists:
            flash(f"That email is already on our mailing list!", "success")
            return redirect(url_for('about'))
        if not exists:
            new_sub = emailList(email = form2.email2.data)
            try:
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('contact'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('contact'))

    if form3.validate_on_submit():
        msg = Message('Home Page Contact Message From ' + form3.name3.data, recipients=['crtechsolutions01@gmail.com'])
        msg.html = '<h3>Contact Message</h3> <br> <h4>Email:' + form3.email3.data + '</h4><br><h4>Name:' + form3.name3.data + '</h4> <br> <p>' + form3.message3.data + '</p>'
        mail.send(msg)
        flash(f'Your Message has been sent!  Thank you for your interest in Flow - Accounting Simplified!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form, form2=form2, form3=form3)

@app.route('/services', methods=['GET', 'POST'])
def services():
    form = ContactForm()
    form2 = EmailListForm()

    if form.validate_on_submit():
        msg = Message('Home Page Contact Message From ' + form.name.data, recipients=['crtechsolutions01@gmail.com'])
        msg.html = '<h3>Contact Message</h3> <br> <h4>Email:' + form.email.data + '</h4><br><h4>Name:' + form.name.data + '</h4> <br> <p>' + form.message.data + '</p>'
        mail.send(msg)
        flash(f'Your Message has been sent!  Thank you for your interest in Flow - Accounting Simplified!', 'success')
        return redirect(url_for('services'))

    if form2.validate_on_submit():
        exists = emailList.query.filter(emailList.email == form2.email2.data).first()
        if exists:
            flash(f"That email is already on our mailing list!", "success")
            return redirect(url_for('services'))
        if not exists:
            new_sub = emailList(email = form2.email2.data)
            try:
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('services'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_sub)
                db.session.commit()
                db.session.flush()
                flash(f'{form2.email2.data} has been added to our mailing list!', 'success')
                return redirect(url_for('services'))

    return render_template('services.html', form=form, form2=form2)

# ROUTE FOR PDF OF MANUAL TO BE DOWNLOADED
@app.route('/pdf/Flow_Operating_Manual.pdf', methods=['GET'])
def flowManual():
    return render_template('pdf/Flow_Operating_Manual.pdf')