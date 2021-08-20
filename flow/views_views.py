import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import *
from flow.models import *
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import *
from flow.sorting import *
from decimal import *

@app.route('/view/customers', methods=['GET', 'POST'])
@login_required
def viewCustomers():
    try:
        customers = customerTable.query.filter_by(userid=current_user.id).order_by(asc(customerTable.accountnumber)).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        customers = customerTable.query.filter_by(userid=current_user.id).order_by(asc(customerTable.accountnumber)).all()
    form = CustomerModifyForm()

    if form.validate_on_submit():
        accountnumber = form.accountnumber.data

        try:
            existtest = customerTable.query.filter(customerTable.accountnumber == accountnumber).filter(customerTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            existtest = customerTable.query.filter(customerTable.accountnumber == accountnumber).filter(customerTable.userid == current_user.id).first()

        if not existtest:
            flash(f'Error: That account number does not exist.', 'error')
            return redirect(url_for('viewCustomers'))
        else:
            try:
                customer = customerTable.query.filter(customerTable.accountnumber == accountnumber).filter(customerTable.userid == current_user.id).first()
                customer.customername = form.customername.data
                customer.customerdescription = form.customerdescription.data
                customer.customeremail = form.email.data
                customer.customeraddress = form.address.data
                customer.customercity = form.city.data
                customer.customerstate = form.state.data
                customer.customerzip = form.zip.data
                customer.customerterm = form.term.data
                customer.customernumber = form.number.data
                db.session.flush()
                db.session.commit()
                flash(f'Customer Modified!', 'success')
                return redirect(url_for('viewCustomers'))
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                customer = customerTable.query.filter(customerTable.accountnumber == accountnumber).filter(customerTable.userid == current_user.id).first()
                customer.customername = form.customername.data
                customer.customerdescription = form.customerdescription.data
                customer.customeremail = form.email.data
                customer.customeraddress = form.address.data
                customer.customercity = form.city.data
                customer.customerstate = form.state.data
                customer.customerzip = form.zip.data
                customer.customerterm = form.term.data
                customer.customernumber = form.number.data
                db.session.flush()
                db.session.commit()
                flash(f'Customer Modified!', 'success')
                return redirect(url_for('viewCustomers'))
            
    return render_template('/view/customers.html', rows=customers, form=form)

@app.route('/view/vendors', methods=['GET', 'POST'])
@login_required
def viewVendors():
    try:
        vendors = vendorTable.query.filter_by(userid=current_user.id).order_by(asc(vendorTable.accountnumber)).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        vendors = vendorTable.query.filter_by(userid=current_user.id).order_by(asc(vendorTable.accountnumber)).all()
    table = VendorResults(vendors)
    form = VendorModifyForm()

    if form.validate_on_submit():
        accountnumber = form.accountnumber.data
        vendorname = form.vendorname.data
        vendordescription = form.vendordescription.data

        try:
            existtest = vendorTable.query.filter(vendorTable.accountnumber == accountnumber).filter(vendorTable.userid == current_user.id).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            existtest = vendorTable.query.filter(vendorTable.accountnumber == accountnumber).filter(vendorTable.userid == current_user.id).first()

        if not existtest:
            flash(f'Error: That account number does not exist.', 'error')
            return redirect(url_for('viewCustomers'))
        else:
            try:
                vendor = vendorTable.query.filter(vendorTable.accountnumber == accountnumber).filter(vendorTable.userid == current_user.id).first()
                vendor.vendorname = vendorname
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                vendor = vendorTable.query.filter(vendorTable.accountnumber == accountnumber).filter(vendorTable.userid == current_user.id).first()
                vendor.vendorname = vendorname
                db.session.flush()
                db.session.commit()

            try:
                vendor = vendorTable.query.filter(vendorTable.accountnumber == accountnumber).filter(vendorTable.userid == current_user.id).first()
                vendor.vendordescription = vendordescription
                db.session.flush()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                vendor = vendorTable.query.filter(vendorTable.accountnumber == accountnumber).filter(vendorTable.userid == current_user.id).first()
                vendor.vendordescription = vendordescription
                db.session.flush()
                db.session.commit()
            flash(f'Vendor Modified!', 'success')
            return redirect(url_for('viewVendors'))
    return render_template('/view/vendors.html', table=table, form=form)

@app.route('/view/debts', methods=['GET', 'POST'])
@login_required
def viewDebts():
    try:
        debts = debtTable.query.filter_by(userid=current_user.id).order_by(asc(debtTable.accountnumber)).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        debts = debtTable.query.filter_by(userid=current_user.id).order_by(asc(debtTable.accountnumber)).all()
    form = DebtDeleteForm()
    add2 = Decimal(10) ** -2

    for debt in debts:
        new = Decimal(debt.debtamount).quantize(add2)
        debt.debtamount = "{:,}".format(new)

    if form.validate_on_submit():
        try:
            debttest = debtTable.query.filter(customerTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debttest = debtTable.query.filter(customerTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).first()

        if debttest:
            try:
                debtdelete = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).delete()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                debtdelete = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.accountnumber == form.accountnumber.data).delete()
                db.session.commit()
            flash(f'Debt Deleted!', 'success')
            return redirect(url_for('viewDebts'))
        else:
            flash(f'Error: Check your information, could not find debt matching that account number.', 'error')
            return redirect(url_for('viewDebts'))
            
    return render_template('/view/debts.html', rows = debts, form=form)

@app.route('/view/investments', methods=['GET', 'POST'])
@login_required
def viewInvestments():
    try:
        investments = investmentTable.query.filter_by(userid=current_user.id).order_by(asc(investmentTable.accountnumber)).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        investments = investmentTable.query.filter_by(userid=current_user.id).order_by(asc(investmentTable.accountnumber)).all()
    add2 = Decimal(10) ** -2

    form = InvestmentDeleteForm()

    if form.validate_on_submit():
        try:
            investmenttest = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.accountnumber == form.accountnumber.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            investmenttest = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.accountnumber == form.accountnumber.data).first()

        if investmenttest:
            try:
                investmentdelete = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.accountnumber == form.accountnumber.data).delete()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                investmentdelete = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.accountnumber == form.accountnumber.data).delete()
                db.session.commit()
            flash(f'Investment Deleted!', 'success')
            return redirect(url_for('viewInvestments'))
        else:
            flash(f'Error: Check your information, could not find investment matching that account number.', 'error')
            return redirect(url_for('viewInvestments'))
    
    for inv in investments:
        new = Decimal(inv.investmentamount).quantize(add2)
        inv.investmentamount = "{:,}".format(new)
            
    return render_template('/view/investments.html', rows = investments, form=form)

@app.route('/view/equipment', methods=['GET', 'POST'])
@login_required
def viewEquipment():
    try:
        props = propertyTable.query.filter_by(userid=current_user.id).order_by(desc(propertyTable.propertydate)).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        props = propertyTable.query.filter_by(userid=current_user.id).order_by(desc(propertyTable.propertydate)).all()
    add2 = Decimal(10) ** -2

    for prop in props:
        new = Decimal(prop.propertycost).quantize(add2)
        prop.propertycost = "{:,}".format(new)

    form = PropertyDeleteForm()

    if form.validate_on_submit():
        try:
            propertytest = propertyTable.query.filter(propertyTable.userid == current_user.id).filter(propertyTable.propertyid == form.propertyid.data).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            propertytest = propertyTable.query.filter(propertyTable.userid == current_user.id).filter(propertyTable.propertyid == form.propertyid.data).first()
        if propertytest:
            try:
                propertydelete = propertyTable.query.filter(propertyTable.userid == current_user.id).filter(propertyTable.propertyid == form.propertyid.data).delete()
                db.session.commit()
            except(AttributeError, SQLAlchemy.exc.OperationalError):
                propertydelete = propertyTable.query.filter(propertyTable.userid == current_user.id).filter(propertyTable.propertyid == form.propertyid.data).delete()
                db.session.commit()
            flash(f'Property Deleted!', 'success')
            return redirect(url_for('viewEquipment'))
        else:
            flash(f'Error: Check your information, could not find that property id.', 'error')
            return redirect(url_for('viewEquipment'))
            
    return render_template('/view/equipment.html', form=form, rows = props)

@app.route('/view/receivables', methods=['GET', 'POST'])
@login_required
def viewReceivables():
    form = RecPayPaid()
    form2 = RecPayDelete()
    try:
        recs = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).order_by(asc(accountsReceivableTable.invoicenumber)).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        recs = accountsReceivableTable.query.filter(accountsReceivableTable.userid == current_user.id).order_by(asc(accountsReceivableTable.invoicenumber)).all()
    add2 = Decimal(10) ** -2

    for rec in recs:
        new = Decimal(rec.totalamount).quantize(add2)
        rec.totalamount = "{:,}".format(new)
    
    if form.validate_on_submit():
        return redirect(url_for('newIncomeReceivable'))
    
    if form2.validate_on_submit():
        return redirect(url_for('newIncomeReceivable'))
            
    return render_template('/view/receivables.html', rows = recs, form=form, form2=form2)

@app.route('/view/payables', methods=['GET', 'POST'])
@login_required
def viewPayables():
    form = RecPayPaid()
    form2 = RecPayDelete()
    try:
        pays = accountsPayableTable.query.filter(accountsPayableTable.userid == current_user.id).order_by(asc(accountsPayableTable.duedate)).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        pays = accountsPayableTable.query.filter(accountsPayableTable.userid == current_user.id).order_by(asc(accountsPayableTable.duedate)).all()
    add2 = Decimal(10) ** -2

    for pay in pays:
        new = Decimal(pay.totalamount).quantize(add2)
        pay.totalamount = "{:,}".format(new)
    
    if form.validate_on_submit():
        return redirect(url_for('newExpensePayable'))
    
    if form2.validate_on_submit():
        return redirect(url_for('newExpensePayable'))
            
    return render_template('/view/payables.html', rows = pays, form=form, form2=form2)

@app.route('/view/balances', methods=['GET'])
@login_required
def viewBalances():
    try:
        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).limit(365)
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        bals = balanceTable.query.filter(balanceTable.userid == current_user.id).order_by(desc(balanceTable.date)).limit(365)
    add2 = Decimal(10) ** -2

    for bal in bals:
        new = Decimal(bal.bankbalance).quantize(add2)
        bal.bankbalance = "{:,}".format(new)

    return render_template('/view/balances.html', rows = bals)