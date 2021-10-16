import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flask_mail import Mail, Message
from flow.forms import *
from flow.models import usersTable, subuserTable, accountTable, transactionTable, investmentTable, debtTable, customerTable, vendorTable, bankTable
from flow import app, db, bcrypt, bootstrap, mail
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import AccountResults, TransactionResults, CustomerResults, DebtResults, VendorResults
from flow.sorting import sort7day, sortmonth, sortthreemonth, sortsixmonth, sortyear, sortthreeyear, sortfiveyear, addTotals
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import *
import calendar

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = usersTable.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            try:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('overview'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('overview'))
        else:
            flash('Login Unsuccessful.  Please check your credentials.', 'error')
    return render_template('login.html', form=form)

def save_logo(form_logo):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_logo.filename)
    logo_fn = random_hex + f_ext
    logo_path = os.path.join(app.root_path, 'static/business_logos', logo_fn)
    form_logo.save(logo_path)
    return logo_fn


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        if form.businesslogo.data:
            logo = save_logo(form.businesslogo.data)
        else:
            logo = 'default_logo.png'
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = usersTable(fname=form.firstname.data, lname=form.lastname.data, email=form.email.data, username=form.username.data, 
                              password=hashed_password, joined=date.today(), businessname=form.businessname.data, 
                              businessnumber=0, businessaddress = form.businessaddress.data, businesscity=form.businesscity.data, businesszip=form.businesszip.data, businessstate = form.businessstate.data, businesswebsite=form.businesswebsite.data, 
                              fiscalyearstart=form.fiscalyearstart.data, fiscalyearend=form.fiscalyearend.data, businesslogo=logo, member=True)
        try:
            db.session.add(new_user)
            db.session.commit()
            newuser = usersTable.query.filter(usersTable.email == form.email.data).first()
            account1000 = accountTable(userid = newuser.id, accountnumber = 1000, accountname = 'Utilities', accountdescription = 'Power, Water, etc.', accountdate = date.today(), main = True, mainname = 'Utilities')
            db.session.add(account1000)
            account2000 = accountTable(userid = newuser.id, accountnumber = 2000, accountname = 'Accounts Payable', accountdescription = 'Expenses', accountdate = date.today(), main = True, mainname = 'Accounts Payable')
            db.session.add(account2000)
            account3000 = accountTable(userid = newuser.id, accountnumber = 3000, accountname = 'Accounts Receivable', accountdescription = 'Income', accountdate = date.today(), main = True, mainname = 'Accounts Receivable')
            db.session.add(account3000)
            newbank = bankTable(userid = newuser.id, accountnumber = 1, bankname = form.bankname.data, bankbalance = form.bankbalance.data, bankdate = date.today())
            db.session.add(newbank)
            newbalance = balanceTable(userid = newuser.id, bankname = form.bankname.data, bankbalance = form.bankbalance.data, date = date.today())
            db.session.add(newbalance)
            db.session.commit()
            flash(f'Congratulations {form.businessname.data}, your account has been created, and Chart of Accounts started! Be sure to start your subscription to use Flow!', 'success')
            return redirect(url_for('login'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_user)
            db.session.commit()
            newuser = usersTable.query.filter(usersTable.email == form.email.data).first()
            account1000 = accountTable(userid = newuser.id, accountnumber = 1000, accountname = 'Utilities', accountdescription = 'Power, Water, etc.', accountdate = date.today(), main = True, mainname = 'Utilities')
            db.session.add(account1000)
            account2000 = accountTable(userid = newuser.id, accountnumber = 2000, accountname = 'Accounts Payable', accountdescription = 'Expenses', accountdate = date.today(), main = True, mainname = 'Accounts Payable')
            db.session.add(account2000)
            account3000 = accountTable(userid = newuser.id, accountnumber = 3000, accountname = 'Accounts Receivable', accountdescription = 'Income', accountdate = date.today(), main = True, mainname = 'Accounts Receivable')
            db.session.add(account3000)
            newbank = bankTable(userid = newuser.id, accountnumber = 1, bankname = form.bankname.data, bankbalance = form.bankbalance.data, bankdate = date.today())
            db.session.add(newbank)
            newbalance = balanceTable(userid = newuser.id, bankname = form.bankname.data, bankbalance = form.bankbalance.data, date = date.today())
            db.session.add(newbalance)
            db.session.commit()
            flash(f'Congratulations {form.businessname.data}, your account has been created, and Chart of Accounts started! Be sure to start your subscription to use Flow!', 'success')
            return redirect(url_for('login'))

    return render_template('sign_up.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/business-info', methods=['GET', 'POST'])
@login_required
def businessInfo():
    form2 = ChangePassword()
    form3 = ChangeEmail()
    form4 = ChangeBusinessName()
    form6 = ChangeBusinessWebsite()
    form7 = UpdateBalance()
    form8 = UpdateFiscal()
    form9 = UpdateLogo()
    form10 = ChangeBusinessAddress()

    add2 = Decimal(10) ** -2
    
    business_logo = url_for('static', filename='assets/business_logos/' + current_user.businesslogo)

    if form2.validate_on_submit():
        try:
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            if user and bcrypt.check_password_hash(user.password, form2.currentpassword.data):
                hashed_password = bcrypt.generate_password_hash(form2.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.flush()
                db.session.commit()
                flash(f'The password has been updated.', 'success')
                return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            if user and bcrypt.check_password_hash(user.password, form2.currentpassword.data):
                hashed_password = bcrypt.generate_password_hash(form2.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.flush()
                db.session.commit()
                flash(f'The password has been updated.', 'success')
                return redirect(url_for('businessInfo'))
        else:
            flash(f'The current password is incorrect.', 'error')
            return redirect(url_for('businessInfo'))
    
    if form3.validate_on_submit():
        try:
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            if user.email == form3.currentemail.data:
                user.email = form3.newemail.data
                db.session.flush()
                db.session.commit()
                flash(f'The email has been updated', 'success')
                return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            if user.email == form3.currentemail.data:
                user.email = form3.newemail.data
                db.session.flush()
                db.session.commit()
                flash(f'The email has been updated', 'success')
                return redirect(url_for('businessInfo'))
        else:
            (flash(f'Your current email did not match, if you keep having this problem please notify us within Feedback -> Bug Reports', 'error'))
            return redirect(url_for('businessInfo'))
        
    if form4.validate_on_submit():
        try:
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.businessname = form4.newname.data
            db.session.flush()
            db.session.commit()
            flash(f'The business name has been updated to: ' + form4.newname.data, 'success')
            return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.businessname = form4.newname.data
            db.session.flush()
            db.session.commit()
            flash(f'The business name has been updated to: ' + form4.newname.data, 'success')
            return redirect(url_for('businessInfo'))
    
    if form6.validate_on_submit():
        try:
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.businesswebsite = form6.newsite.data
            db.session.flush()
            db.session.commit()
            flash(f'The business website has been updated to: ' + form6.newsite.data, 'success')
            return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.businesswebsite = form6.newsite.data
            db.session.flush()
            db.session.commit()
            flash(f'The business website has been updated to: ' + form6.newsite.data, 'success')
            return redirect(url_for('businessInfo'))
    
    if form7.validate_on_submit():
        try:
            user = bankTable.query.filter(bankTable.userid == current_user.id).first()
            user.bankbalance = form7.newbalance.data
            db.session.flush()
            db.session.commit()
            newbal = Decimal(user.bankbalance).quantize(add2)
            flash(f'The current balance has been updated to: $' + "{:,}".format(newbal), 'success')
            return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = bankTable.query.filter(bankTable.userid == current_user.id).first()
            user.bankbalance = form7.newbalance.data
            db.session.flush()
            db.session.commit()
            newbal = Decimal(user.bankbalance).quantize(add2)
            flash(f'The current balance has been updated to: $' + "{:,}".format(newbal), 'success')
            return redirect(url_for('businessInfo'))
    
    if form8.validate_on_submit():
        try:
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.fiscalyearstart = form8.startyear.data
            user.fiscalyearend = form8.endyear.data
            db.session.flush()
            db.session.commit()
            flash(f'Your fiscal year has been updated to: ' + str(form8.startyear.data) + ' -> ' + str(form8.endyear.data) ,'success')
            return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.fiscalyearstart = form8.startyear.data
            user.fiscalyearend = form8.endyear.data
            db.session.flush()
            db.session.commit()
            flash(f'Your fiscal year has been updated to: ' + str(form8.startyear.data) + ' -> ' + str(form8.endyear.data) ,'success')
            return redirect(url_for('businessInfo'))
    
    if form9.validate_on_submit():
        try:
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            if user.businesslogo == 'default_logo.png':
                logo = save_logo(form9.businesslogo.data)
                user=usersTable.query.filter(usersTable.id == current_user.id).first()
                user.businesslogo = logo
                db.session.flush()
                db.session.commit()
                flash(f'Your logo has been updated!', 'success')
                return redirect(url_for('businessInfo'))
            elif user.businesslogo != 'default_logo.png':
                logo_path = os.path.join(app.root_path, 'static/business_logos', current_user.businesslogo)
                exists = os.path.exists(logo_path)
                if exists:
                    os.remove(os.path.join(app.root_path, 'static/business_logos', current_user.businesslogo))
                    logo = save_logo(form9.businesslogo.data)
                    user=usersTable.query.filter(usersTable.id == current_user.id).first()
                    user.businesslogo = logo
                    db.session.flush()
                    db.session.commit()
                    flash(f'Your logo has been updated!', 'success')
                    return redirect(url_for('businessInfo'))
                if not exists:
                    logo = save_logo(form9.businesslogo.data)
                    user=usersTable.query.filter(usersTable.id == current_user.id).first()
                    user.businesslogo = logo
                    db.session.flush()
                    db.session.commit()
                    flash(f'Your logo has been updated!', 'success')
                    return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            if user.businesslogo == 'default_logo.png':
                logo = save_logo(form9.businesslogo.data)
                user=usersTable.query.filter(usersTable.id == current_user.id).first()
                user.businesslogo = logo
                db.session.flush()
                db.session.commit()
                flash(f'Your logo has been updated!', 'success')
                return redirect(url_for('businessInfo'))
            elif user.businesslogo != 'default_logo.png':
                logo_path = os.path.join(app.root_path, 'static/business_logos', current_user.businesslogo)
                exists = os.path.exists(logo_path)
                if exists:
                    os.remove(os.path.join(app.root_path, 'static/business_logos', current_user.businesslogo))
                    logo = save_logo(form9.businesslogo.data)
                    user=usersTable.query.filter(usersTable.id == current_user.id).first()
                    user.businesslogo = logo
                    db.session.flush()
                    db.session.commit()
                    flash(f'Your logo has been updated!', 'success')
                    return redirect(url_for('businessInfo'))
                if not exists:
                    logo = save_logo(form9.businesslogo.data)
                    user=usersTable.query.filter(usersTable.id == current_user.id).first()
                    user.businesslogo = logo
                    db.session.flush()
                    db.session.commit()
                    flash(f'Your logo has been updated!', 'success')
                    return redirect(url_for('businessInfo'))
    if form10.validate_on_submit():
        try:
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.businessaddress = form10.newaddress.data
            user.businesscity = form10.newcity.data
            user.businessstate = form10.newstate.data
            user.businesszip = form10.newzip.data
            db.session.flush()
            db.session.commit()
            flash(f'Your address has been updated successfully!' ,'success')
            return redirect(url_for('businessInfo'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == current_user.id).first()
            user.businessaddress = form10.newaddress.data
            user.businesscity = form10.newcity.data
            user.businessstate = form10.newstate.data
            user.businesszip = form10.newzip.data
            db.session.flush()
            db.session.commit()
            flash(f'Your address has been updated successfully!' ,'success')
            return redirect(url_for('businessInfo'))


    return render_template('business-info.html', business_logo=business_logo, form2 = form2, form3 = form3, form4 = form4, form6 = form6, form7=form7, form8 = form8, form9 = form9, form10 = form10)

@app.route('/process_cancellation', methods=['POST'])
@login_required
def processCancellation():
    msg = Message('Membership Cancellation of ' + current_user.username, recipients=['chase@chasecoding.com'])
    msg.html = '<h3>Account Manager, <br>Please cancel the membership of user: <i>\'' + current_user.username + '\'</i>, their userid is: ' + str(current_user.id) + '</h3>. <br> <br> <small>*This email is not checked, please do not respond.</small>'
    mail.send(msg)
    flash(f'Your cancellation has been started, please give us 24 to 72 hours to finalize the cancellation.  We are sorry our product wasn\'t a good fit for you, please leave us feedback on how we can improve!', 'success')
    return redirect(url_for('businessInfo'))

@app.route('/process_bug_report', methods=['POST', 'GET'])
@login_required
def processBugReport():
    bugtype = request.args.get('bugtype')
    report = request.args.get('report')
    msg = Message('Bug Report from ' + current_user.username, recipients=['chase@chasecoding.com'])
    msg.html = '<h3>Account Manager, <br>The bug report was sent by: <i>\'' + current_user.username + '\'</i>, their userid is: ' + str(current_user.id) + '</h3>. <br> <h4>Bug Type: <i>' + bugtype + '</i></h4> <br> <br> <h4>Bug Report:</h4> <br>' + report + '<br>' + '<br> <br> <small>*This email is not checked, please do not respond.</small>'
    mail.send(msg)
    new_bug_report = bugReportTable(userid = current_user.id, bugtype = bugtype, bugdescription = report, bugdate = date.today())
    try:
        db.session.add(new_bug_report)
        db.session.commit()
        flash(f'Your bug report was sent!  Thank you for taking the time to help us improve Flow!', 'success')
        return redirect(url_for('bugReport'))
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        db.session.add(new_bug_report)
        db.session.commit()
        flash(f'Your bug report was sent!  Thank you for taking the time to help us improve Flow!', 'success')
        return redirect(url_for('bugReport'))

@app.route('/process_feedback', methods=['POST', 'GET'])
@login_required
def processFeedback():
    feedback = request.args.get('feedback')
    msg = Message('Feedback from ' + current_user.username, recipients=['chase@chasecoding.com'])
    msg.html = '<h3>Account Manager, <br>The feedback was sent by: <i>\'' + current_user.username + '\'</i>, their userid is: ' + str(current_user.id)  + '.</h3> <br> <h4>Feedback:</h4> <br>' + feedback + '<br> <br> <br> <small>*This email is not checked, please do not respond.</small>'
    mail.send(msg)
    new_feedback = feedbackTable(userid = current_user.id, feedback = feedback, feedbackdate = date.today())
    try:
        db.session.add(new_feedback)
        db.session.commit()
        flash(f'Your feedback was submitted!  Thank you so much for your feedback, it helps us grow and continue to improve!', 'success')
        return redirect(url_for('feedback'))
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        db.session.add(new_feedback)
        db.session.commit()
        flash(f'Your feedback was submitted!  Thank you so much for your feedback, it helps us grow and continue to improve!', 'success')
        return redirect(url_for('feedback'))

@app.route('/start_subscription', methods=['POST', 'GET'])
@login_required
def subscribe():
    form = MembershipIssueButton()

    if form.validate_on_submit():
        msg = Message('Membership Problem from ' + current_user.username, recipients=['chase@chasecoding.com'])
        msg.html = '<h3>Account Manager, <br>The Membership problem was sent by: <i>\'' + current_user.username + '\'</i>, their userid is: ' + str(current_user.id) + '</h3>. <br> <h4></h4> <br> <br> <h4>Please check to see if they did have a payment. Their <b>EMAIL ADDRESS</b> is <b> ' + current_user.email + ' and make sure they are members if they did. Contact them and figure out how they paid, then cross check it with the PayPal recurring payments dashboard. </b></h4> <br><br>' + '<br> <br> <small>*This email is not checked, please do not respond.</small>'
        mail.send(msg)
        new_bug_report = bugReportTable(userid = current_user.id, bugtype = 'Membership Problem', bugdescription = 'Payment not changing membership', bugdate = date.today())
        try:
            db.session.add(new_bug_report)
            db.session.commit()
            flash(f'The issue was sent to our account management team.  They will get back to you as soon as possible!', 'success')
            return redirect(url_for('subscribe'))
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_bug_report)
            db.session.commit()
            flash(f'The issue was sent to our account management team.  They will get back to you as soon as possible!', 'success')
            return redirect(url_for('subscribe'))
    return render_template('/start_subscription.html', form=form)

# @app.route('/process_subscription', methods=['GET','POST'])
# @login_required
# def processSubscription():
#     try:
#         user = usersTable.query.filter(usersTable.id == current_user.id).first()
#         user.member = True
#         user.lastpaydate = date.today()
#         db.session.flush()
#         db.session.commit()
#         msg = Message('Membership Started for ' + current_user.username + '!', recipients=['chase@chasecoding.com', 'gameradvocat3@gmail.com'])
#         msg.html = 'New member added!'
#         mail.send(msg)
#         return redirect(url_for('overview'))
#     except(AttributeError, SQLAlchemy.exc.OperationalError):
#         user = usersTable.query.filter(usersTable.id == current_user.id).first()
#         user.member = True
#         user.lastpaydate = date.today()
#         db.session.flush()
#         db.session.commit()
#         msg = Message('Membership Started for ' + current_user.username + '!', recipients=['chase@chasecoding.com', 'gameradvocat3@gmail.com'])
#         msg.html = 'New member added!'
#         mail.send(msg)
#         return redirect(url_for('overview'))

# reset password email function
def sendResetEmail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f'''
This link expires 15 minutes after being sent. To reset your password, click the link below:

{url_for('resetPassword', token = token, _external=True)}

If you did not submit this request, simply ignore this message and no changes will occur..  This is only sent to your email.
'''
    mail.send(msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgotPassword():
    form = RequestResetForm()

    if form.validate_on_submit():
        email = str(form.email.data)
        try:
            user = usersTable.query.filter(usersTable.email == email).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.email == email).first()
        if user:
            sendResetEmail(user)
            flash(f'An email has been sent with instructions to reset your password!', 'success')
            return redirect(url_for('login'))
        if not user:
            flash(f'There was no account associated with that email. Please register to use Flow.', 'error')
            return redirect(url_for('forgotPassword'))

    return render_template('/forgot_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    user = usersTable.verify_reset_token(token)

    if user is None:
        flash(f'That is an invalid or expired link.', 'error')
        return redirect(url_for('forgotPassword'))
    
    form = PasswordResetForm()

    if form.validate_on_submit():
        if form.password.data:
            try:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.flush()
                db.session.commit()
                flash(f'The password has been updated.', 'success')
                return redirect(url_for('login'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.flush()
                db.session.commit()
                flash(f'The password has been updated.', 'success')
                return redirect(url_for('login'))
        else:
            flash(f'There was an error processing your request, if this keeps occurring please contact us.', 'error')
            return redirect(url_for('forgotPassword'))

    return render_template('/reset_password.html', form=form)