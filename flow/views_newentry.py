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

@app.route('/new_entry/new-transaction', methods=['GET'])
@login_required
def newTransaction():
    return render_template('new_entry/new-transaction.html')

@app.route('/mobile/new_entry/new-transaction', methods=['GET'])
@login_required
def mobileNewTransaction():
    return render_template('/mobile/new_entry/new-transaction.html')

@app.route('/new_entry/new-account', methods=['GET', 'POST'])
@login_required
def newAccount():
    form = AccountForm()

    privstart = 0
    privend = 3999
    reservedrangestart = 100000
    reservedrangeend = 299999
    maxallowed = 999999

    if form.validate_on_submit():
        anum = form.accountnumber.data
        try:
            accountnumberval = accountTable.query.filter_by(accountnumber=form.accountnumber.data).filter_by(userid=current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            accountnumberval = accountTable.query.filter_by(accountnumber=form.accountnumber.data).filter_by(userid=current_user.id).first()
        if anum >= reservedrangestart and anum <= reservedrangeend:
            flash(f'Error: You tried to use a reserved account number.  0 - 3999 and 100000 - 299999 are reserved for internal use.', 'error')
            return redirect(url_for('newAccount'))
        if anum >= privstart and anum <= privend:
            flash(f'Error: You tried to use a reserved account number.  0 - 100 and 100000 - 299999 are reserved for internal use.', 'error')
            return redirect(url_for('newAccount'))
        if anum > maxallowed:
            flash(f'Error: You went over the allowable account number range, please choose a different account number.', 'error')
            return redirect(url_for('newAccount'))
        if accountnumberval:
            flash(f'Error: The account number has already been assigned to another account.', 'error')
            return redirect(url_for('newAccount'))
        else:
            new_account = accountTable(user=current_user, accountnumber=form.accountnumber.data, accountname=form.accountname.data, 
                                       accountdescription=form.description.data, accountdate=form.date.data, main=True, mainname = form.accountname.data)
            try:
                db.session.add(new_account)
                db.session.commit()
                flash(f'The account has been created!', 'success')
                return redirect(url_for('newAccount'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_account)
                db.session.commit()
                flash(f'The account has been created!', 'success')
                return redirect(url_for('newAccount'))
        
    return render_template('/new_entry/new-account.html', form=form)

@app.route('/mobile/new_entry/new-account', methods=['GET', 'POST'])
@login_required
def mobileNewAccount():
    form = AccountForm()

    privstart = 0
    privend = 3999
    reservedrangestart = 100000
    reservedrangeend = 299999
    maxallowed = 999999

    if form.validate_on_submit():
        anum = form.accountnumber.data
        try:
            accountnumberval = accountTable.query.filter_by(accountnumber=form.accountnumber.data).filter_by(userid=current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            accountnumberval = accountTable.query.filter_by(accountnumber=form.accountnumber.data).filter_by(userid=current_user.id).first()
        if anum >= reservedrangestart and anum <= reservedrangeend:
            flash(f'Error: You tried to use a reserved account number.  0 - 3999 and 100000 - 299999 are reserved for internal use.', 'error')
            return redirect(url_for('mobileNewAccount'))
        if anum >= privstart and anum <= privend:
            flash(f'Error: You tried to use a reserved account number.  0 - 100 and 100000 - 299999 are reserved for internal use.', 'error')
            return redirect(url_for('mobileNewAccount'))
        if anum > maxallowed:
            flash(f'Error: You went over the allowable account number range, please choose a different account number.', 'error')
            return redirect(url_for('mobileNewAccount'))
        if accountnumberval:
            flash(f'Error: The account number has already been assigned to another account.', 'error')
            return redirect(url_for('mobileNewAccount'))
        else:
            new_account = accountTable(user=current_user, accountnumber=form.accountnumber.data, accountname=form.accountname.data, 
                                       accountdescription=form.description.data, accountdate=form.date.data, main=True, mainname = form.accountname.data)
            try:
                db.session.add(new_account)
                db.session.commit()
                flash(f'The account has been created!', 'success')
                return redirect(url_for('mobileNewAccount'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_account)
                db.session.commit()
                flash(f'The account has been created!', 'success')
                return redirect(url_for('mobileNewAccount'))
        
    return render_template('/mobile/new_entry/new-account.html', form=form)

@app.route('/new_entry/new-vendor', methods=['GET', 'POST'])
@login_required
def newVendor():
    form = VendorForm()
    form.accountsignature.choices = [(account.mainname, str(account.accountnumber) + '-' + account.accountname) for account in accountTable.query.filter(accountTable.userid == current_user.id).filter_by(main = True).all()]

    if form.validate_on_submit():
        try:
            vendorvalidate = vendorTable.query.filter(vendorTable.userid == current_user.id).filter(vendorTable.vendorname == form.vendorname.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendorvalidate = vendorTable.query.filter(vendorTable.userid == current_user.id).filter(vendorTable.vendorname == form.vendorname.data).first()
        if vendorvalidate:
            flash(f'{form.vendorname.data} is already the name of a vendor in your list', 'error')
            return redirect(url_for('newVendor'))
        else:
            account = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.mainname == form.accountsignature.data).order_by(desc(accountTable.accountnumber)).first()
            newaccountnumber = account.accountnumber + 1
            new_account = accountTable(user=current_user, accountnumber=newaccountnumber, accountname=form.vendorname.data, accountdescription=form.description.data, accountdate=date.today(), main = False, mainname = form.accountsignature.data)
            new_vendor = vendorTable(user=current_user, accountnumber=newaccountnumber, vendorname=form.vendorname.data, vendordescription=form.description.data, vendordate=date.today())
            try:
                db.session.add(new_account, new_vendor)
                db.session.commit()
                flash(f'{form.vendorname.data} has been added to your vendor list!', 'success')
                return redirect(url_for('newVendor'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_account, new_vendor)
                db.session.commit()
                flash(f'{form.vendorname.data} has been added to your vendor list!', 'success')
                return redirect(url_for('newVendor'))
    return render_template('new_entry/new-vendor.html', form=form)

@app.route('/mobile/new_entry/new-vendor', methods=['GET', 'POST'])
@login_required
def mobileNewVendor():
    form = VendorForm()
    form.accountsignature.choices = [(account.mainname, str(account.accountnumber) + '-' + account.accountname) for account in accountTable.query.filter(accountTable.userid == current_user.id).filter_by(main = True).all()]

    if form.validate_on_submit():
        try:
            vendorvalidate = vendorTable.query.filter(vendorTable.userid == current_user.id).filter(vendorTable.vendorname == form.vendorname.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendorvalidate = vendorTable.query.filter(vendorTable.userid == current_user.id).filter(vendorTable.vendorname == form.vendorname.data).first()
        if vendorvalidate:
            flash(f'{form.vendorname.data} is already the name of a vendor in your list', 'error')
            return redirect(url_for('mobileNewVendor'))
        else:
            account = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.mainname == form.accountsignature.data).order_by(desc(accountTable.accountnumber)).first()
            newaccountnumber = account.accountnumber + 1
            new_account = accountTable(user=current_user, accountnumber=newaccountnumber, accountname=form.vendorname.data, accountdescription=form.description.data, accountdate=date.today(), main = False, mainname = form.accountsignature.data)
            new_vendor = vendorTable(user=current_user, accountnumber=newaccountnumber, vendorname=form.vendorname.data, vendordescription=form.description.data, vendordate=date.today())
            try:
                db.session.add(new_account, new_vendor)
                db.session.commit()
                flash(f'{form.vendorname.data} has been added to your vendor list!', 'success')
                return redirect(url_for('mobileNewVendor'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_account, new_vendor)
                db.session.commit()
                flash(f'{form.vendorname.data} has been added to your vendor list!', 'success')
                return redirect(url_for('mobileNewVendor'))
    return render_template('/mobile/new_entry/new-vendor.html', form=form)

@app.route('/new_entry/new-customer', methods=['GET', 'POST'])
@login_required
def newCustomer():
    form = CustomerForm()
    form.accountsignature.choices = [(account.mainname, str(account.accountnumber) + '-' + account.accountname) for account in accountTable.query.filter(accountTable.userid == current_user.id).filter_by(main = True).all()]

    if form.validate_on_submit():
        try:
            customervalidate = customerTable.query.filter(customerTable.userid == current_user.id).filter(customerTable.customername == form.customername.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customervalidate = customerTable.query.filter(customerTable.userid == current_user.id).filter(customerTable.customername == form.customername.data).first()
        if customervalidate:
            flash(f'{form.customername.data} is already the name of a customer in your list', 'error')
            return redirect(url_for('newCustomer'))
        else:
            account = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.mainname == form.accountsignature.data).order_by(desc(accountTable.accountnumber)).first()
            newaccountnumber = account.accountnumber + 1
            new_account = accountTable(user=current_user, accountnumber=newaccountnumber, accountname=form.customername.data, accountdescription=form.description.data, accountdate=date.today(), main = False, mainname = form.accountsignature.data)
            new_customer = customerTable(user=current_user, accountnumber=newaccountnumber, customername=form.customername.data, customerdescription=form.description.data, \
                            customerdate=date.today(), customeraddress = form.address.data, customercity = form.city.data, customerstate = form.state.data, customerzip = form.zip.data, \
                            customernumber = form.number.data, customeremail = form.email.data)
            try:    
                db.session.add(new_account, new_customer)
                db.session.commit()
                flash(f'{form.customername.data} has been added to your customer list!', 'success')
                return redirect(url_for('newCustomer'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_account, new_customer)
                db.session.commit()
                flash(f'{form.customername.data} has been added to your customer list!', 'success')
                return redirect(url_for('newCustomer'))
    return render_template('new_entry/new-customer.html', form=form)

@app.route('/mobile/new_entry/new-customer', methods=['GET', 'POST'])
@login_required
def mobileNewCustomer():
    form = CustomerForm()
    form.accountsignature.choices = [(account.mainname, str(account.accountnumber) + '-' + account.accountname) for account in accountTable.query.filter(accountTable.userid == current_user.id).filter_by(main = True).all()]

    if form.validate_on_submit():
        try:
            customervalidate = customerTable.query.filter(customerTable.userid == current_user.id).filter(customerTable.customername == form.customername.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customervalidate = customerTable.query.filter(customerTable.userid == current_user.id).filter(customerTable.customername == form.customername.data).first()
        if customervalidate:
            flash(f'{form.customername.data} is already the name of a customer in your list', 'error')
            return redirect(url_for('mobileNewCustomer'))
        else:
            account = accountTable.query.filter(accountTable.userid == current_user.id).filter(accountTable.mainname == form.accountsignature.data).order_by(desc(accountTable.accountnumber)).first()
            newaccountnumber = account.accountnumber + 1
            new_account = accountTable(user=current_user, accountnumber=newaccountnumber, accountname=form.customername.data, accountdescription=form.description.data, accountdate=date.today(), main = False, mainname = form.accountsignature.data)
            new_customer = customerTable(user=current_user, accountnumber=newaccountnumber, customername=form.customername.data, customerdescription=form.description.data, customerdate=date.today())
            try:
                db.session.add(new_account, new_customer)
                db.session.commit()
                flash(f'{form.customername.data} has been added to your customer list!', 'success')
                return redirect(url_for('mobileNewCustomer'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_account, new_customer)
                db.session.commit()
                flash(f'{form.customername.data} has been added to your customer list!', 'success')
                return redirect(url_for('mobileNewCustomer'))
    return render_template('/mobile/new_entry/new-customer.html', form=form)


@app.route('/new_entry/new-income', methods=['GET', 'POST'])
@login_required
def newIncome():
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    def addAccountNumber(customerid):
        try:
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        return '{}'.format(customer.accountnumber)
    def addCustomerName(customerid):
        try:
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        return '{}'.format(customer.customername)

    form = TransactionIncomeForm()
    form.transactionsource.choices = [(customer.customerid, customer.customername) for customer in customerTable.query.filter(customerTable.userid == current_user.id).all()]

    if form.validate_on_submit():
        if form.totalamount.data >= 0:
            accountnumber = addAccountNumber(form.transactionsource.data)
            customername = addCustomerName(form.transactionsource.data)
            new_transaction = transactionTable(userid=current_user.id, accountid=accountnumber, transactiontype='Income', 
                                            transactionsource=customername, transactiondescription=form.transactiondescription.data, 
                                            pretaxtotal=form.pretaxtotal.data, salestax=form.salestax.data, totalamount=form.totalamount.data, 
                                            transactiondate=form.transactiondate.data, transactionmethod=form.transactionmethod.data,
                                            transactionreason=form.transactionreason.data)
            try:
                db.session.add(new_transaction)
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
                bank.bankbalance = bank.bankbalance + form.totalamount.data
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_transaction)
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
                bank.bankbalance = bank.bankbalance + form.totalamount.data
                db.session.commit()

            try:
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == form.transactiondate.data).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == form.transactiondate.data).first()
            if not balance:
                try:
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                
                if earliest.date > form.transactiondate.data:
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance + form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance += form.totalamount.data
                    try:
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        db.session.flush()
                        db.session.commit()
                elif latest.date > form.transactiondate.data > earliest.date:
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance + form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance += form.totalamount.data
                    try:
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        db.session.flush()
                        db.session.commit()
            elif balance:
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance += form.totalamount.data
                db.session.flush()
                db.session.commit()
            flash(f'The transaction was added!', 'success')
            return redirect(url_for('newIncome'))
        elif form.totalamount.data < 0:
            flash(f'You entered a number below 0, please enter a positive amount.', 'error')
            return redirect(url_for('newIncome'))
    return render_template('new_entry/new-income.html', form=form)

@app.route('/mobile/new_entry/new-income', methods=['GET', 'POST'])
@login_required
def mobileNewIncome():
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    def addAccountNumber(customerid):
        try:
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        return '{}'.format(customer.accountnumber)
    def addCustomerName(customerid):
        try:
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        return '{}'.format(customer.customername)

    form = TransactionIncomeForm()
    form.transactionsource.choices = [(customer.customerid, customer.customername) for customer in customerTable.query.filter(customerTable.userid == current_user.id).all()]

    if form.validate_on_submit():
        if form.totalamount.data >= 0:
            accountnumber = addAccountNumber(form.transactionsource.data)
            customername = addCustomerName(form.transactionsource.data)
            new_transaction = transactionTable(userid=current_user.id, accountid=accountnumber, transactiontype='Income', 
                                            transactionsource=customername, transactiondescription=form.transactiondescription.data, 
                                            pretaxtotal=form.pretaxtotal.data, salestax=form.salestax.data, totalamount=form.totalamount.data, 
                                            transactiondate=form.transactiondate.data, transactionmethod=form.transactionmethod.data,
                                            transactionreason=form.transactionreason.data)
            try:
                db.session.add(new_transaction)
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
                bank.bankbalance = bank.bankbalance + form.totalamount.data
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_transaction)
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
                bank.bankbalance = bank.bankbalance + form.totalamount.data
                db.session.commit()

            try:
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == form.transactiondate.data).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == form.transactiondate.data).first()
            if not balance:
                try:
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                
                if earliest.date > form.transactiondate.data:
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance + form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance += form.totalamount.data
                    try:
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        db.session.flush()
                        db.session.commit()
                elif latest.date > form.transactiondate.data > earliest.date:
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance + form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance += form.totalamount.data
                    try:
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        db.session.flush()
                        db.session.commit()
            elif balance:
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance += form.totalamount.data
                try:
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    db.session.flush()
                    db.session.commit()
            flash(f'The transaction was added!', 'success')
            return redirect(url_for('newIncome'))
        elif form.totalamount.data < 0:
            flash(f'You entered a number below 0, please enter a positive amount.', 'error')
            return redirect(url_for('mobileNewIncome'))
    return render_template('mobile/new_entry/new-income.html', form=form)

@app.route('/new_entry/new-income-receivable', methods=['GET', 'POST'])
@login_required
def newIncomeReceivable():
    if 'transactionnumber' in request.args and 'transactiondate' in request.args:
        transnum = request.args.get('transactionnumber')
        transdate1 = request.args.get('transactiondate')
        transdate2 = datetime.strptime(transdate1, '%Y-%m-%d')
        transdate = datetime.strftime(transdate2, '%Y-%m-%d')
        try:
            reccheck = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.invoicenumber == transnum).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            reccheck = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.invoicenumber == transnum).first()
        if reccheck:
            try:
                transaction = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.invoicenumber == transnum).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                transaction = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.invoicenumber == transnum).first()
            new_transaction = transactionTable(userid=current_user.id, accountid=transaction.accountid, transactiontype='Income', 
                                            transactionsource=transaction.transactionsource, transactiondescription=transaction.transactiondescription, 
                                            pretaxtotal=transaction.pretaxtotal, salestax=transaction.salestax, totalamount=transaction.totalamount, 
                                            transactiondate=transdate2, transactionmethod=transaction.transactionmethod,
                                            transactionreason=transaction.transactionreason)
            db.session.add(new_transaction)
            try:
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance + transaction.totalamount
            try:
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.flush()
                db.session.commit()

            try:
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == transdate).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == transdate).first()

            if not balance:
                try:
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()

                earliest = datetime.strftime(earliest1.date, '%Y-%m-%d')
                latest = datetime.strftime(latest1.date, '%Y-%m-%d')
                
                if earliest > transdate:
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance + transaction.totalamount, date = transdate)
                    db.session.add(newbal)
                    try:
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()

                    for bal in bals:
                        bal.bankbalance += transaction.totalamount

                    try:
                        db.session.flush()
                        db.session.commit
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        db.session.flush()
                        db.session.commit
                elif latest > transdate > earliest:
                    try:
                        nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < transdate).order_by(desc(balanceTable.date)).first()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < transdate).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance + transaction.totalamount, date = datetime.date(transdate))
                    db.session.add(newbal)
                    try:
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()
                    for bal in bals:
                        bal.bankbalance += transaction.totalamount

                    try:
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        db.session.flush()
                        db.session.commit()
            elif balance:
                try:
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transdate).all()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transdate).all()
                for bal in bals:
                    bal.bankbalance += transaction.totalamount
                    try:
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        db.session.flush()
                        db.session.commit()

            try:
                reccheck.paid = True
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                reccheck.paid = True
                db.session.flush()
                db.session.commit()

            flash(f'Marked as Paid!', 'success')
            return redirect(url_for('viewReceivables'))
        if not reccheck:
            flash(f'There was an error, check your information.', 'error')
            return redirect(url_for('viewReceivables'))
        
    if 'transactionnumber2' in request.args:
        transnum = request.args.get('transactionnumber2')
        try:
            reccheck = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.invoicenumber == transnum).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            reccheck = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).filter(accountsReceivableTable.invoicenumber == transnum).first()
        if reccheck:
            try:
                receivabledelete = accountsReceivableTable.query.filter(accountsReceivableTable.invoicenumber == transnum).filter(accountsReceivableTable.userid == current_user.id).delete()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                receivabledelete = accountsReceivableTable.query.filter(accountsReceivableTable.invoicenumber == transnum).filter(accountsReceivableTable.userid == current_user.id).delete()
            
            db.session.flush()
            db.session.commit()

            flash(f'Receivable Deleted!', 'success')
            return redirect(url_for('viewReceivables'))
        if not reccheck:
            flash(f'There was an error, check your information.', 'error')
            return redirect(url_for('viewReceivables'))
    else:
        flash(f'There was an error, check your information', 'error')
        return redirect(url_for('viewReceivables'))
    
    return render_template('new_entry/new-income-receivable.html')

@app.route('/new_entry/new-expense', methods=['GET', 'POST'])
@login_required
def newExpense():
    def addAccountNumber(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.accountnumber)
    def addVendorName(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.vendorname)
    form = TransactionExpenseForm()
    form.transactionsource.choices = [(vendor.vendorid, vendor.vendorname) for vendor in vendorTable.query.filter(vendorTable.userid == current_user.id).all()]

    if form.validate_on_submit():
        accountnumber = addAccountNumber(form.transactionsource.data)
        vendorname = addVendorName(form.transactionsource.data)

        new_expense_transaction = transactionTable(userid=current_user.id, accountid=accountnumber, transactiontype='Expense', 
                                           transactionsource=vendorname, transactiondescription=form.transactiondescription.data, 
                                           pretaxtotal=form.pretaxtotal.data, salestax=form.salestax.data, totalamount=form.totalamount.data, 
                                           transactiondate=form.transactiondate.data, transactionmethod=form.transactionmethod.data,
                                           transactionreason=form.transactionreason.data)
        try:
            db.session.add(new_expense_transaction)
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.totalamount.data
            db.session.flush()
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_expense_transaction)
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.totalamount.data
            db.session.flush()
            db.session.commit()
        
        try:
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()
        if not balance:
            try:
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            
            if earliest.date > form.transactiondate.data:
                try:
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
            elif latest.date > form.transactiondate.data > earliest.date:
                try:
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
        elif balance:
            try:
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.totalamount.data
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.totalamount.data
                db.session.flush()
                db.session.commit()
        flash(f'The transaction was added!', 'success')
        return redirect(url_for('newExpense'))
    return render_template('new_entry/new-expense.html', form=form)

@app.route('/mobile/new_entry/new-expense', methods=['GET', 'POST'])
@login_required
def mobileNewExpense():
    def addAccountNumber(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.accountnumber)
    def addVendorName(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.vendorname)
    form = TransactionExpenseForm()
    form.transactionsource.choices = [(vendor.vendorid, vendor.vendorname) for vendor in vendorTable.query.filter(vendorTable.userid == current_user.id).all()]

    if form.validate_on_submit():
        accountnumber = addAccountNumber(form.transactionsource.data)
        vendorname = addVendorName(form.transactionsource.data)

        new_expense_transaction = transactionTable(userid=current_user.id, accountid=accountnumber, transactiontype='Expense', 
                                           transactionsource=vendorname, transactiondescription=form.transactiondescription.data, 
                                           pretaxtotal=form.pretaxtotal.data, salestax=form.salestax.data, totalamount=form.totalamount.data, 
                                           transactiondate=form.transactiondate.data, transactionmethod=form.transactionmethod.data,
                                           transactionreason=form.transactionreason.data)
        try:
            db.session.add(new_expense_transaction)
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.totalamount.data
            db.session.flush()
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_expense_transaction)
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.totalamount.data
            db.session.flush()
            db.session.commit()
        
        try:
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()
        if not balance:
            try:
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            
            if earliest.date > form.transactiondate.data:
                try:
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
            elif latest.date > form.transactiondate.data > earliest.date:
                try:
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.totalamount.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.totalamount.data
                    db.session.flush()
                    db.session.commit()
            flash(f'The transaction was added!', 'success')
            return redirect(url_for('mobileNewExpense'))
        elif balance:
            try:
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.totalamount.data
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.totalamount.data
                db.session.flush()
                db.session.commit()
            flash(f'The transaction was added!', 'success')
            return redirect(url_for('mobileNewExpense'))
    return render_template('mobile/new_entry/new-expense.html', form=form)

@app.route('/new_entry/new-expense-payable', methods=['GET', 'POST'])
@login_required
def newExpensePayable():
    if 'transactionnumber' in request.args and 'transactiondate' in request.args:
        transnum = request.args.get('transactionnumber')
        transdate1 = request.args.get('transactiondate')
        transdate2 = datetime.strptime(transdate1, '%Y-%m-%d')
        transdate = datetime.strftime(transdate2, '%Y-%m-%d')
        try:
            reccheck = accountsPayableTable.query.filter(accountsPayableTable.transactionid == transnum).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            reccheck = accountsPayableTable.query.filter(accountsPayableTable.transactionid == transnum).first()

        if reccheck:
            try:
                transaction = accountsPayableTable.query.filter(accountsPayableTable.userid == current_user.id).filter(accountsPayableTable.transactionid == transnum).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                transaction = accountsPayableTable.query.filter(accountsPayableTable.userid == current_user.id).filter(accountsPayableTable.transactionid == transnum).first()
            new_transaction = transactionTable(userid=current_user.id, accountid=transaction.accountid, transactiontype='Expense', 
                                            transactionsource=transaction.transactionsource, transactiondescription=transaction.transactiondescription, 
                                            pretaxtotal=transaction.pretaxtotal, salestax=transaction.salestax, totalamount=transaction.totalamount, 
                                            transactiondate=transdate2, transactionmethod=transaction.transactionmethod,
                                            transactionreason=transaction.transactionreason)
            try:
                db.session.add(new_transaction)
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
                bank.bankbalance = bank.bankbalance - transaction.totalamount
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                db.session.add(new_transaction)
                bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
                bank.bankbalance = bank.bankbalance - transaction.totalamount
                db.session.flush()
                db.session.commit()
                
            try:
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == transdate).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == transdate).first()

            if not balance:
                try:
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                    earliest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                    latest1 = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                earliest = datetime.strftime(earliest1.date, '%Y-%m-%d')
                latest = datetime.strftime(latest1.date, '%Y-%m-%d')
                
                if earliest > transdate:
                    try:
                        newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - transaction.totalamount, date = transdate)
                        db.session.add(newbal)
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()
                        for bal in bals:
                            bal.bankbalance -= transaction.totalamount
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - transaction.totalamount, date = transdate)
                        db.session.add(newbal)
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()
                        for bal in bals:
                            bal.bankbalance -= transaction.totalamount
                        db.session.flush()
                        db.session.commit()
                elif latest > transdate > earliest:
                    try:
                        nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < transdate).order_by(desc(balanceTable.date)).first()
                        newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - transaction.totalamount, date = datetime.date(transdate))
                        db.session.add(newbal)
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()
                        for bal in bals:
                            bal.bankbalance -= transaction.totalamount
                        db.session.flush()
                        db.session.commit()
                    except(AttributeError, SQLAlchemy.exc.OperationalError):
                        nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < transdate).order_by(desc(balanceTable.date)).first()
                        newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - transaction.totalamount, date = datetime.date(transdate))
                        db.session.add(newbal)
                        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > transdate).all()
                        for bal in bals:
                            bal.bankbalance -= transaction.totalamount
                        db.session.flush()
                        db.session.commit()
            elif balance:
                try:
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transdate).all()
                    for bal in bals:
                        bal.bankbalance -= transaction.totalamount
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= transdate).all()
                    for bal in bals:
                        bal.bankbalance -= transaction.totalamount
                    db.session.flush()
                    db.session.commit()

            try:
                reccheck.paid = True
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                reccheck.paid = True
                db.session.flush()
                db.session.commit()
            flash(f'Marked as Paid!', 'success')
            return redirect(url_for('viewPayables'))
        if not reccheck:
            flash(f'There was an error, check your information.', 'error')
            return redirect(url_for('viewPayables'))
        
    if 'transactionnumber2' in request.args:
        transnum = request.args.get('transactionnumber2')
        try:
            paycheck = accountsPayableTable.query.filter(accountsPayableTable.transactionid == transnum).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            paycheck = accountsPayableTable.query.filter(accountsPayableTable.transactionid == transnum).first()
        if paycheck:
            try:
                payabledelete = accountsPayableTable.query.filter(accountsPayableTable.transactionid == transnum).filter(accountsPayableTable.userid == current_user.id).delete()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                payabledelete = accountsPayableTable.query.filter(accountsPayableTable.transactionid == transnum).filter(accountsPayableTable.userid == current_user.id).delete()
                db.session.commit()
            flash(f'Payable Deleted!', 'success')
            return redirect(url_for('viewPayables'))
        if not paycheck:
            flash(f'There was an error, check your information.', 'error')
            return redirect(url_for('viewPayables'))
    else:
        flash(f'There was an error, check your information', 'error')
        return redirect(url_for('viewPayables'))
    return render_template('new_entry/new-expense-payable.html')

@app.route('/new_entry/new-debt-payment', methods=['GET', 'POST'])
@login_required
def newDebtPayment():
    def paymentinterest(payment, apr):
        percent = apr / 100
        interest = payment * percent
        return interest

    def paymentprinciple(payment, apr):
        percent = apr / 100
        interest = payment * percent
        principle = payment - interest
        return principle

    form = TransactionDebtForm()
    add2 = Decimal(10) ** -2
    form.accountnumber.choices = [(str(debt.accountnumber), (str(debt.accountnumber) + ' - ' + debt.debtvendor + ' - ' + '$' + str(Decimal(debt.debtamount).quantize(add2)))) for debt in debtTable.query.filter(debtTable.userid == current_user.id).all()]

    if form.validate_on_submit():

        try:
            debt = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debt = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
        vendorname = debt.debtvendor

        interest = paymentinterest(form.payment.data, debt.debtapr)
        principle = paymentprinciple(form.payment.data, debt.debtapr)

        try:
            debt_mod = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
            debt_mod.debtamount = Decimal(debt_mod.debtamount - principle).quantize(add2)
            debt_mod.interestpaid = Decimal(debt_mod.interestpaid + interest).quantize(add2)
            db.session.flush()
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debt_mod = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
            debt_mod.debtamount = Decimal(debt_mod.debtamount - principle).quantize(add2)
            debt_mod.interestpaid = Decimal(debt_mod.interestpaid + interest).quantize(add2)
            db.session.flush()
            db.session.commit()
        

        new_expense_transaction = transactionTable(userid=current_user.id, accountid=form.accountnumber.data, transactiontype='Expense', 
                                                   transactionsource=vendorname, transactiondescription='Debt Payment', 
                                                   pretaxtotal=0, salestax=0, totalamount=form.payment.data, 
                                                   transactiondate=form.transactiondate.data, transactionmethod=form.transactionmethod.data,
                                                   transactionreason='Other Expense')
        try:
            db.session.add(new_expense_transaction)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_expense_transaction)
            db.session.commit()

        try:
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.payment.data
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.payment.data

        try:
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()

        if not balance:
            try:
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            
            if earliest.date > form.transactiondate.data:
                try:
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
            elif latest.date > form.transactiondate.data > earliest.date:
                try:
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
        elif balance:
            try:
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.payment.data
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.payment.data
                db.session.flush()
                db.session.commit()
        
        flash(f'The Debt Payment was Logged!', 'success')
        return redirect(url_for('newDebtPayment'))
    return render_template('new_entry/new-debt-payment.html', form=form)

@app.route('/mobile/new_entry/new-debt-payment', methods=['GET', 'POST'])
@login_required
def mobileNewDebtPayment():
    def paymentinterest(payment, apr):
        percent = apr / 100
        interest = payment * percent
        return interest

    def paymentprinciple(payment, apr):
        percent = apr / 100
        interest = payment * percent
        principle = payment - interest
        return principle

    form = TransactionDebtForm()
    add2 = Decimal(10) ** -2
    form.accountnumber.choices = [(str(debt.accountnumber), (str(debt.accountnumber) + ' - ' + debt.debtvendor + ' - ' + '$' + str(Decimal(debt.debtamount).quantize(add2)))) for debt in debtTable.query.filter(debtTable.userid == current_user.id).all()]

    if form.validate_on_submit():

        try:
            debt = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debt = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
        vendorname = debt.debtvendor

        interest = paymentinterest(form.payment.data, debt.debtapr)
        principle = paymentprinciple(form.payment.data, debt.debtapr)

        try:
            debt_mod = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
            debt_mod.debtamount = Decimal(debt_mod.debtamount - principle).quantize(add2)
            debt_mod.interestpaid = Decimal(debt_mod.interestpaid + interest).quantize(add2)
            db.session.flush()
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debt_mod = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
            debt_mod.debtamount = Decimal(debt_mod.debtamount - principle).quantize(add2)
            debt_mod.interestpaid = Decimal(debt_mod.interestpaid + interest).quantize(add2)
            db.session.flush()
            db.session.commit()
        

        new_expense_transaction = transactionTable(userid=current_user.id, accountid=form.accountnumber.data, transactiontype='Expense', 
                                                   transactionsource=vendorname, transactiondescription='Debt Payment', 
                                                   pretaxtotal=0, salestax=0, totalamount=form.payment.data, 
                                                   transactiondate=form.transactiondate.data, transactionmethod=form.transactionmethod.data,
                                                   transactionreason='Other Expense')
        try:
            db.session.add(new_expense_transaction)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_expense_transaction)
            db.session.commit()

        try:
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.payment.data
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
            bank.bankbalance = bank.bankbalance - form.payment.data

        try:
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).first()

        if not balance:
            try:
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).first()
            
            if earliest.date > form.transactiondate.data:
                try:
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
            elif latest.date > form.transactiondate.data > earliest.date:
                try:
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.transactiondate.data).order_by(desc(balanceTable.date)).first()
                    newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance - form.payment.data, date = form.transactiondate.data)
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.transactiondate.data).all()
                    for bal in bals:
                        bal.bankbalance -= form.payment.data
                    db.session.flush()
                    db.session.commit()
        elif balance:
            try:
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.payment.data
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.transactiondate.data).all()
                for bal in bals:
                    bal.bankbalance -= form.payment.data
                db.session.flush()
                db.session.commit()
        
        flash(f'The Debt Payment was Logged!', 'success')
        return redirect(url_for('mobileNewDebtPayment'))
    return render_template('/mobile/new_entry/new-debt-payment.html', form=form)

@app.route('/new_entry/new-owner-investment', methods=['GET', 'POST'])
@login_required
def newOwnerInvestment():
    def addAccountNumber(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.accountnumber)
    def addVendorName(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.vendorname)

    form = InvestmentForm()

    if form.validate_on_submit():
        try:
            accounttest = investmentTable.query.filter(investmentTable.userid == current_user.id).order_by(desc(investmentTable.accountnumber)).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            accounttest = investmentTable.query.filter(investmentTable.userid == current_user.id).order_by(desc(investmentTable.accountnumber)).first()
        newaccountnumber = 0

        if not accounttest:
            newaccountnumber = 200001
        else:
            newaccountnumber = accounttest.accountnumber + 1
        
        new_transaction = transactionTable(userid=current_user.id, accountid=newaccountnumber, transactiontype='Investment', transactionsource=form.fname.data + ' ' + form.lname.data,
                                     transactiondescription=form.description.data, totalamount =form.amount.data, transactiondate=form.date.data,
                                     transactionmethod=form.method.data, pretaxtotal=0, salestax=0, transactionreason='Other Income')
        new_equity = investmentTable(user=current_user, accountnumber=newaccountnumber, fname=form.fname.data, lname=form.lname.data, investmentamount=form.amount.data, investmentdescription=form.description.data,
                                     investmentdate=form.date.data)
        try:
            db.session.add(new_transaction, new_equity)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_transaction, new_equity)
            db.session.commit()
        
        try:
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            bank = bankTable.query.filter(bankTable.userid == current_user.id).first()
        
        try:
            bank.bankbalance = bank.bankbalance + form.amount.data
            db.session.flush()
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            bank.bankbalance = bank.bankbalance + form.amount.data
            db.session.flush()
            db.session.commit()

        try:
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == form.date.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date == form.date.data).first()

        if not balance:
            try:
                bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bankname = bankTable.query.filter(bankTable.userid == current_user.id).first()
                earliest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
                latest = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(asc(balanceTable.date)).first()
            
            if earliest.date > form.date.data:
                newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = earliest.bankbalance + form.amount.data, date = form.date.data)
                try:
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.date.data).all()
                    for bal in bals:
                        bal.bankbalance += form.amount.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    db.session.add(newbal)
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.date.data).all()
                    for bal in bals:
                        bal.bankbalance += form.amount.data
                    db.session.flush()
                    db.session.commit()
            elif latest.date > form.date.data > earliest.date:
                try:
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.date.data).order_by(desc(balanceTable.date)).first()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    nextbal = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date < form.date.data).order_by(desc(balanceTable.date)).first()
                newbal = balanceTable(userid = current_user.id, bankname = bankname.bankname, bankbalance = nextbal.bankbalance + form.amount.data, date = form.date.data)
                db.session.add(newbal)
                try:
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.date.data).all()
                    for bal in bals:
                        bal.bankbalance += form.amount.data
                    db.session.flush()
                    db.session.commit()
                except(AttributeError, SQLAlchemy.exc.OperationalError):
                    bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date > form.date.data).all()
                    for bal in bals:
                        bal.bankbalance += form.amount.data
                    db.session.flush()
                    db.session.commit()
        elif balance:
            try:
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.date.data).all()
                for bal in bals:
                    bal.bankbalance += form.amount.data
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                bals = balanceTable.query.filter(balanceTable.userid == current_user.id).filter(balanceTable.date >= form.date.data).all()
                for bal in bals:
                    bal.bankbalance += form.amount.data
                db.session.flush()
                db.session.commit()
        flash(f'The investment was added!', 'success')
        return redirect(url_for('newOwnerInvestment'))
    return render_template('new_entry/new-owner-investment.html', form=form)

@app.route('/new_entry/new-long-term-debt', methods=['GET', 'POST'])
@login_required
def newLongTermDebt():
    def addAccountNumber(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.accountnumber)
    def addVendorName(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.vendorname)

    form = DebtForm()

    form.vendorname.choices = [(str(vendor.accountnumber) + '-' + vendor.vendorname, str(vendor.accountnumber) + '-' + vendor.vendorname) for vendor in vendorTable.query.filter(vendorTable.userid == current_user.id).all()]

    if form.validate_on_submit():
        try:
            accounttest = debtTable.query.filter(debtTable.userid == current_user.id).order_by(desc(debtTable.accountnumber)).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            accounttest = debtTable.query.filter(debtTable.userid == current_user.id).order_by(desc(debtTable.accountnumber)).first()
        newaccountnumber = 0

        if not accounttest:
            newaccountnumber = 100001
        else:
            newaccountnumber = accounttest.accountnumber + 1

        add2 = Decimal(10) ** -2

        new_debt = debtTable(user=current_user, accountnumber=newaccountnumber, debtvendor=form.vendorname.data, debtdescription=form.description.data, debtapr=form.apr.data, 
                             debtamount=Decimal(form.amount.data).quantize(add2), debtdate=form.date.data, interestpaid = 0)
        try:
            db.session.add(new_debt)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_debt)
            db.session.commit()
        flash(f'The debt was added!', 'success')
        return redirect(url_for('newLongTermDebt'))
    return render_template('new_entry/new-long-term-debt.html', form=form)

@app.route('/new_entry/new-equipment', methods=['GET', 'POST'])
@login_required
def newEquipment():
    form = PropertyForm()

    if form.validate_on_submit():
        
        if form.propertylife.data >= 50 or form.propertylife.data < 0:
            flash(f'Please enter a value less than 50 years.', 'error')
            return redirect(url_for('newEquipment'))

        new_property = propertyTable(userid=current_user.id, propertyname = form.propertyname.data,
                                     propertydescription = form.propertydescription.data, propertycost = form.propertycost.data,
                                     propertydate = form.propertydate.data, propertylife = form.propertylife.data)
        try:
            db.session.add(new_property)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_property)
            db.session.commit()
        flash(f'The asset {form.propertyname.data} was added!', 'success')
        return redirect(url_for('newEquipment'))
    return render_template('new_entry/new-equipment.html', form=form)

@app.route('/mobile/new_entry/new-equipment', methods=['GET', 'POST'])
@login_required
def mobileNewEquipment():
    form = PropertyForm()

    if form.validate_on_submit():
        
        if form.propertylife.data >= 50 or form.propertylife.data < 0:
            flash(f'Please enter a value less than 50 years.', 'error')
            return redirect(url_for('newEquipment'))

        new_property = propertyTable(userid=current_user.id, propertyname = form.propertyname.data,
                                     propertydescription = form.propertydescription.data, propertycost = form.propertycost.data,
                                     propertydate = form.propertydate.data, propertylife = form.propertylife.data)
        try:
            db.session.add(new_property)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_property)
            db.session.commit()
        flash(f'The asset {form.propertyname.data} was added!', 'success')
        return redirect(url_for('mobileNewEquipment'))
    return render_template('/mobile/new_entry/new-equipment.html', form=form)

@app.route('/new_entry/new-receivable', methods=['GET', 'POST'])
@login_required
def newReceivable():
    def addAccountNumber(customerid):
        customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        return '{}'.format(customer.accountnumber)
    def addCustomerName(customerid):
        customer = customerTable.query.filter(customerTable.customerid == customerid).filter(customerTable.userid == current_user.id).first()
        return '{}'.format(customer.customername)
    form = ReceivableForm()
    form.transactionsource.choices = [(customer.customerid, customer.customername) for customer in customerTable.query.filter(customerTable.userid == current_user.id).all()]

    def assignInvoice():
        inv = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).order_by(desc(accountsReceivableTable.invoicenumber)).first()

        if not inv:
            invoicenumber = 1
            return invoicenumber
        if inv:
            invoicenumber = inv.invoicenumber + 1
            return invoicenumber

    if form.validate_on_submit():
        accountnumber = addAccountNumber(form.transactionsource.data)
        customername = addCustomerName(form.transactionsource.data)
        new_receivable = accountsReceivableTable(userid=current_user.id, accountid=accountnumber, transactiontype='Income', 
                                           transactionsource=customername, transactiondescription=form.transactiondescription.data, 
                                           pretaxtotal=form.pretaxtotal.data, salestax=form.salestax.data, totalamount=form.totalamount.data, 
                                           duedate=form.duedate.data, transactionmethod=form.transactionmethod.data,
                                           transactionreason=form.transactionreason.data, paid=False, invoicenumber = assignInvoice())
        try:
            db.session.add(new_receivable)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_receivable)
            db.session.commit()
        flash(f'The open Invoice was added!', 'success')
        return redirect(url_for('newReceivable'))
    return render_template('new_entry/new-receivable.html', form=form)

@app.route('/new_entry/new-payable', methods=['GET', 'POST'])
@login_required
def newPayable():
    def addAccountNumber(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.accountnumber)
    def addVendorName(vendorid):
        try:
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            vendor = vendorTable.query.filter(vendorTable.vendorid == vendorid).first()
        return '{}'.format(vendor.vendorname)
    form = PayableForm()
    form.transactionsource.choices = [(vendor.vendorid, vendor.vendorname) for vendor in vendorTable.query.filter(vendorTable.userid == current_user.id).all()]

    if form.validate_on_submit():
        accountnumber = addAccountNumber(form.transactionsource.data)
        vendorname = addVendorName(form.transactionsource.data)

        new_payable = accountsPayableTable(userid=current_user.id, accountid=accountnumber, transactiontype='Expense', 
                                           transactionsource=vendorname, transactiondescription=form.transactiondescription.data, 
                                           pretaxtotal=form.pretaxtotal.data, salestax=form.salestax.data, totalamount=form.totalamount.data, 
                                           duedate=form.duedate.data, transactionmethod=form.transactionmethod.data,
                                           transactionreason=form.transactionreason.data)
        try:
            db.session.add(new_payable)
            db.session.commit()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            db.session.add(new_payable)
            db.session.commit()
        flash(f'The Payable was added!', 'success')
        return redirect(url_for('newPayable'))
    return render_template('new_entry/new-payable.html', form=form)