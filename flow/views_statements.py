import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from flow.forms import *
from flow.models import *
from flow import app, db, bcrypt, bootstrap
from sqlalchemy import update, asc, desc, extract
from flask_login import login_user, current_user, logout_user, login_required
from flow.tables import AccountResults, TransactionResults, CustomerResults, DebtResults, VendorResults, TransactionLog, AccountLog
from flow.sorting import sort7day, sortmonth, sortthreemonth, sortsixmonth, sortyear, sortthreeyear, sortfiveyear, addTotals
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from decimal import *
import calendar

@app.route('/statements', methods=['GET'])
@login_required
def statements():
    return render_template('statements.html')

@app.route('/statements/balance_statement', methods=['GET'])
@login_required
def balanceStatement():
    form = StatementFormRange()

    try:
        fisc = usersTable.query.filter(usersTable.id == current_user.id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        fisc = usersTable.query.filter(usersTable.id == current_user.id).first()

    def findbalance(userid):
        try:
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = bankTable.query.filter(bankTable.userid == userid).first()
        return '{}'.format(balance.bankbalance)
    
    def findsalestax(userid):
        try:
            tran = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= fisc.fiscalyearstart).filter(transactionTable.transactiondate <= fisc.fiscalyearend)
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            tran = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= fisc.fiscalyearstart).filter(transactionTable.transactiondate <= fisc.fiscalyearend)
        salestax = 0
        for trans in tran:
            salestax += trans.salestax
        
        return salestax
    
    def findfiscalstart(userid):
        try:
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        return '{}'.format(fisc.fiscalyearstart)
    
    def findfiscalend(userid):
        try:
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        return '{}'.format(fisc.fiscalyearend)
    
    def findexpenses(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            exps = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Expense').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            exps = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Expense').all()
        expenses = 0
        for exp in exps:
            expenses += exp.totalamount
        
        return expenses
    
    def findrevenue(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            revs = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Income').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            revs = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Income').all()
        revenue = 0
        for rev in revs:
            revenue += rev.totalamount
        
        return revenue
    
    def finddebt(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            debts = debtTable.query.filter(debtTable.userid == userid).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            debts = debtTable.query.filter(debtTable.userid == userid).filter(debtTable.debtamount > 0).all()
        ltd = 0
        for debt in debts:
            ltd += debt.debtamount
        
        return ltd

    def addproperty(userid):
        try:
            props = propertyTable.query.filter(propertyTable.userid == userid).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            props = propertyTable.query.filter(propertyTable.userid == userid).all()
        propvalue = 0
        l_date = date.today()
        for prop in props:
            salvageamount = prop.propertycost * .1
            f_date = prop.propertydate
            delta = l_date - f_date
            diff = delta.days
            years = diff/365
            eol = years/prop.propertylife
            if eol >= 1:
                propvalue = propvalue + (prop.propertycost * .1)
            else:
                salamt = prop.propertycost - salvageamount
                yearlypercentage = 1/prop.propertylife
                yearlydepreciation = salamt * yearlypercentage
                depreciation = yearlydepreciation * years
                propvalue = propvalue + (prop.propertycost - depreciation)
        
        return Decimal(propvalue).quantize(add2)
    
    def addaccountreceivable(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= user.fiscalyearstart).filter(accountsReceivableTable.duedate <= user.fiscalyearend).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= user.fiscalyearstart).filter(accountsReceivableTable.duedate <= user.fiscalyearend).all()
        receivables = 0
        for accs in acc:
            receivables += accs.totalamount
            
        return receivables
        
    def addaccountpayable(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= user.fiscalyearstart).filter(accountsPayableTable.duedate <= user.fiscalyearend).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= user.fiscalyearstart).filter(accountsPayableTable.duedate <= user.fiscalyearend).all()
        payables = 0
        for accs in acc:
            payables += accs.totalamount
        
        return payables
    
    def findequity(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            inv = investmentTable.query.filter(investmentTable.userid == userid).filter(investmentTable.investmentdate >= user.fiscalyearstart).filter(investmentTable.investmentdate <= user.fiscalyearend).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            inv = investmentTable.query.filter(investmentTable.userid == userid).filter(investmentTable.investmentdate >= user.fiscalyearstart).filter(investmentTable.investmentdate <= user.fiscalyearend).all()
        equity = 0
        for invs in inv:
            equity += invs.investmentamount
        
        return equity


    add2 = Decimal(10) ** -2
    
    balance = findbalance(current_user.id)
    bankbalance = Decimal(balance).quantize(add2)
    stax = findsalestax(current_user.id)
    fiscalstart = findfiscalstart(current_user.id)
    fiscalend = findfiscalend(current_user.id)
    expense = findexpenses(current_user.id)
    revenue = findrevenue(current_user.id)
    accrec = addaccountreceivable(current_user.id)
    accpay = addaccountpayable(current_user.id)
    props = addproperty(current_user.id)
    debt = finddebt(current_user.id)
    equity = findequity(current_user.id)

    datestart = fiscalstart
    dateend = fiscalend
    cash = Decimal(bankbalance).quantize(add2)
    accountsreceivable = Decimal(accrec).quantize(add2)
    propertyvalue = Decimal(props).quantize(add2)
    assetstotal = Decimal(float(cash) + float(propertyvalue) + float(accountsreceivable)).quantize(add2)
    accountspayable = Decimal(accpay).quantize(add2)
    expenses = Decimal(expense).quantize(add2)
    salestaxwithholding = Decimal(stax).quantize(add2)
    longtermdebt = Decimal(debt).quantize(add2)
    totalliabilities = Decimal(accountspayable + expenses + salestaxwithholding + longtermdebt).quantize(add2)
    ownersequity = Decimal(equity).quantize(add2)
    revenuetotal = Decimal(revenue).quantize(add2)
    totalequity = Decimal((ownersequity + revenuetotal)).quantize(add2)

    return render_template('/statements/balance_statement.html', datestart = datestart, dateend = dateend, businessname = (current_user.businessname).upper(),
                           cash = "{:,}".format(cash), accountsreceivable = "{:,}".format(accountsreceivable), assetstotal = "{:,}".format(assetstotal), accountspayable = "{:,}".format(accountspayable),
                           expenses = "{:,}".format(expenses), salestaxwithholding = "{:,}".format(salestaxwithholding), longtermdebt = "{:,}".format(longtermdebt),
                           totalliabilities = "{:,}".format(totalliabilities), ownersequity = "{:,}".format(ownersequity), revenuetotal = "{:,}".format(revenuetotal),
                           propertyvalue = "{:,}".format(propertyvalue), totalequity = "{:,}".format(totalequity), form=form)

@app.route('/statements/balance_statement_adjusted', methods=['GET'])
@login_required
def balanceStatementAdjusted():
    form = StatementFormRange()
    startdate = request.args.get('rangestart')
    enddate = request.args.get('rangeend')
    try:
        fisc = usersTable.query.filter(usersTable.id == current_user.id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        fisc = usersTable.query.filter(usersTable.id == current_user.id).first()

    def findbalance(userid):
        try:
            balance = balanceTable.query.filter(balanceTable.userid == userid).filter(balanceTable.date <= enddate).order_by(desc(balanceTable.date)).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            balance = balanceTable.query.filter(balanceTable.userid == userid).filter(balanceTable.date <= enddate).order_by(desc(balanceTable.date)).first()
        if not balance:
            balanceamt = 0.00
        elif balance:
            balanceamt = balance.bankbalance
        return '{}'.format(balanceamt)
    
    def findsalestax(userid):
        try:
            tran = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            tran = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiontype == 'Income').filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).all()
        salestax = 0
        for trans in tran:
            salestax += trans.salestax
        
        return salestax
    
    def findfiscalstart(userid):
        try:
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        return '{}'.format(fisc.fiscalyearstart)
    
    def findfiscalend(userid):
        try:
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            fisc = usersTable.query.filter(usersTable.id == userid).first()
        return '{}'.format(fisc.fiscalyearend)
    
    def findexpenses(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            exps = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Expense').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            exps = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Expense').all()
        expenses = 0
        for exp in exps:
            expenses += exp.totalamount
        
        return expenses
    
    def findrevenue(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            revs = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Income').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            revs = transactionTable.query.filter(transactionTable.userid == userid).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Income').all()
        revenue = 0
        for rev in revs:
            revenue += rev.totalamount
        
        return revenue
    
    def finddebt(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            debts = debtTable.query.filter(debtTable.userid == userid).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            debts = debtTable.query.filter(debtTable.userid == userid).filter(debtTable.debtamount > 0).all()
        ltd = 0
        for debt in debts:
            ltd += debt.debtamount
        
        return ltd

    def addproperty(userid):
        try:
            props = propertyTable.query.filter(propertyTable.userid == userid).filter(propertyTable.propertydate <= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            props = propertyTable.query.filter(propertyTable.userid == userid).filter(propertyTable.propertydate <= enddate).all()
        propvalue = 0
        l_date = datetime.strptime(enddate, '%Y-%m-%d')
        for prop in props:
            salvageamount = prop.propertycost * .1
            f_date = datetime.strptime(str(prop.propertydate), '%Y-%m-%d')
            delta = l_date - f_date
            diff = delta.days
            years = diff/365
            eol = years/prop.propertylife
            if eol >= 1:
                propvalue = propvalue + (prop.propertycost * .1)
            else:
                salamt = prop.propertycost - salvageamount
                yearlypercentage = 1/prop.propertylife
                yearlydepreciation = salamt * yearlypercentage
                depreciation = yearlydepreciation * years
                propvalue = propvalue + (prop.propertycost - depreciation)
        
        return Decimal(propvalue).quantize(add2)
    
    def addaccountreceivable(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= startdate).filter(accountsReceivableTable.duedate <= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= startdate).filter(accountsReceivableTable.duedate <= enddate).all()
        receivables = 0
        for accs in acc:
            receivables += accs.totalamount
            
        return receivables
        
    def addaccountpayable(userid):
        try:
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= startdate).filter(accountsPayableTable.duedate <= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= startdate).filter(accountsPayableTable.duedate <= enddate).all()
        payables = 0
        for accs in acc:
            payables += accs.totalamount
        
        return payables
    
    def findequity(userid):
        try:
            inv = investmentTable.query.filter(investmentTable.userid == userid).filter(investmentTable.investmentdate >= startdate).filter(investmentTable.investmentdate <= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            inv = investmentTable.query.filter(investmentTable.userid == userid).filter(investmentTable.investmentdate >= startdate).filter(investmentTable.investmentdate <= enddate).all()
        equity = 0
        for invs in inv:
            equity += invs.investmentamount
        
        return equity
    
    def figuredebt():
        try:
            debts = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.debtdate <= enddate).filter(debtTable.debtamount > 0).all()
            trans = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.accountid >= 100000).filter(transactionTable.accountid <= 199999).filter(transactionTable.transactiondate >= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == current_user.id).filter(debtTable.debtdate <= enddate).filter(debtTable.debtamount > 0).all()
            trans = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.accountid >= 100000).filter(transactionTable.accountid <= 199999).filter(transactionTable.transactiondate >= enddate).all()
        
        for debt in debts:
            debttotal = 0
            for tran in trans:
                if debt.accountnumber == tran.accountid:
                    apr = tran.totalamount * (1/debt.debtapr)
                    minusapr = tran.totalamount - apr
                    debtamount = debt.debtamount + minusapr
            debttotal += debtamount
        
        return debttotal



    add2 = Decimal(10) ** -2
    
    balance = findbalance(current_user.id)
    bankbalance = Decimal(balance).quantize(add2)
    stax = findsalestax(current_user.id)
    expense = findexpenses(current_user.id)
    revenue = findrevenue(current_user.id)
    accrec = addaccountreceivable(current_user.id)
    accpay = addaccountpayable(current_user.id)
    props = addproperty(current_user.id)
    debt = figuredebt()
    equity = findequity(current_user.id)

    datestart = startdate
    dateend = enddate
    cash = Decimal(bankbalance).quantize(add2)
    accountsreceivable = Decimal(accrec).quantize(add2)
    propertyvalue = Decimal(props).quantize(add2)
    assetstotal = Decimal(float(cash) + float(propertyvalue) + float(accountsreceivable)).quantize(add2)
    accountspayable = Decimal(accpay).quantize(add2)
    expenses = Decimal(expense).quantize(add2)
    salestaxwithholding = Decimal(stax).quantize(add2)
    longtermdebt = Decimal(debt).quantize(add2)
    totalliabilities = Decimal(accountspayable + expenses + salestaxwithholding + longtermdebt).quantize(add2)
    ownersequity = Decimal(equity).quantize(add2)
    revenuetotal = Decimal(revenue).quantize(add2)
    totalequity = Decimal((ownersequity + revenuetotal)).quantize(add2)

    return render_template('/statements/balance_statement_adjusted.html', datestart = datestart, dateend = dateend, businessname = (current_user.businessname).upper(),
                           cash = "{:,}".format(cash), accountsreceivable = "{:,}".format(accountsreceivable), assetstotal = "{:,}".format(assetstotal), accountspayable = "{:,}".format(accountspayable),
                           expenses = "{:,}".format(expenses), salestaxwithholding = "{:,}".format(salestaxwithholding), longtermdebt = "{:,}".format(longtermdebt),
                           totalliabilities = "{:,}".format(totalliabilities), ownersequity = "{:,}".format(ownersequity), revenuetotal = "{:,}".format(revenuetotal),
                           propertyvalue = "{:,}".format(propertyvalue), totalequity = "{:,}".format(totalequity), form=form)

@app.route('/statements/transaction_log', methods=['GET'])
@login_required
def transactionLog():
    form = StatementFormRange()
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        transactions = transactionTable.query.filter_by(userid=current_user.id).order_by(desc(transactionTable.transactiondate)).limit(250).all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        transactions = transactionTable.query.filter_by(userid=current_user.id).order_by(desc(transactionTable.transactiondate)).limit(250).all()
    add2 = Decimal(10) ** -2
    for transaction in transactions:
        new = Decimal(transaction.totalamount).quantize(add2)
        transaction.totalamount = "{:,}".format(new)
    
    return render_template('/statements/transaction_log.html', rows = transactions, form=form, businessname = user.businessname)

@app.route('/statements/transaction_log_adjusted', methods=['GET'])
@login_required
def transactionLogAdjusted():
    startdate = request.args.get('rangestart')
    enddate = request.args.get('rangeend')
    form = StatementFormRange()
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        transactions = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= startdate).\
            filter(transactionTable.transactiondate <= enddate).order_by(desc(transactionTable.transactiondate))
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        transactions = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= startdate).\
            filter(transactionTable.transactiondate <= enddate).order_by(desc(transactionTable.transactiondate))
    add2 = Decimal(10) ** -2
    for transaction in transactions:
        new = Decimal(transaction.totalamount).quantize(add2)
        transaction.totalamount = "{:,}".format(new)
    return render_template('/statements/transaction_log_adjusted.html', rows = transactions, form=form, businessname = user.businessname, startdate = startdate,
                           enddate = enddate)

@app.route('/statements/cash_flow_statement', methods=['GET'])
@login_required
def cashFlowStatement():
    form = StatementFormRange()

    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    add2 = Decimal(10) ** -2

    def getearnings():
        try:
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Income').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Income').all()
        net = 0
        for earn in earnings:
            net += earn.totalamount
        
        return net
    
    def addaccountreceivable(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= user.fiscalyearstart).filter(accountsReceivableTable.duedate <= user.fiscalyearend).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= user.fiscalyearstart).filter(accountsReceivableTable.duedate <= user.fiscalyearend).all()
        receivables = 0
        for accs in acc:
            receivables += accs.totalamount
        
        return receivables
        
    def addaccountpayable(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= user.fiscalyearstart).filter(accountsPayableTable.duedate <= user.fiscalyearend).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= user.fiscalyearstart).filter(accountsPayableTable.duedate <= user.fiscalyearend).all()
        payables = 0
        for accs in acc:
            payables += accs.totalamount
        
        return payables
    
    def addproperty(userid):
        try:
            props = propertyTable.query.filter(propertyTable.userid == userid).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            props = propertyTable.query.filter(propertyTable.userid == userid).all()
        propvalue = 0
        l_date = date.today()
        for prop in props:
            salvageamount = prop.propertycost * .1
            f_date = prop.propertydate
            delta = l_date - f_date
            diff = delta.days
            years = diff/365
            eol = years/prop.propertylife
            if eol >= 1:
                propvalue = propvalue + (prop.propertycost * .1)
            else:
                salamt = prop.propertycost - salvageamount
                yearlypercentage = 1/prop.propertylife
                yearlydepreciation = salamt * yearlypercentage
                depreciation = yearlydepreciation * years
                propvalue = propvalue + (prop.propertycost - depreciation)
        
        return Decimal(propvalue).quantize(add2)
    
    def getexpenses():
        try:
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Expense').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == 'Expense').all()
        net = 0
        for earn in earnings:
            net += earn.totalamount
        
        return net
    

    earns = getearnings()
    accrec = addaccountreceivable(current_user.id)
    accpay = addaccountpayable(current_user.id)
    props = addproperty(current_user.id)
    exp = getexpenses()

    datestart = user.fiscalyearstart
    dateend = user.fiscalyearend
    businessname = (user.businessname).upper()
    netearnings = Decimal(earns).quantize(add2)
    netexpenses = Decimal(exp).quantize(add2)
    accountsreceivable = Decimal(accrec).quantize(add2)
    accountspayable = Decimal(accpay).quantize(add2)
    equipment = Decimal(props).quantize(add2)
    totalcashflow = (netearnings + accountsreceivable + equipment) - (accountspayable + netexpenses)

    if form.validate_on_submit():
        return redirect(url_for('cashFlowStatementAdjusted'))

    return render_template('/statements/cash_flow_statement.html', datestart = datestart, dateend = dateend,
                           netearnings = "{:,}".format(netearnings), accountsreceivable = "{:,}".format(accountsreceivable),
                           accountspayable = "{:,}".format(accountspayable), netexpenses = "{:,}".format(netexpenses), equipment = "{:,}".format(equipment),
                           totalcashflow = "{:,}".format(totalcashflow), businessname = businessname, form=form)

@app.route('/statements/cash_flow_statement_adjusted', methods=['GET'])
@login_required
def cashFlowStatementAdjusted():
    form = StatementFormRange()

    startdate = request.args.get('rangestart')
    enddate = request.args.get('rangeend')

    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    add2 = Decimal(10) ** -2

    def getearnings():
        try:
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Income').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Income').all()
        net = 0
        for earn in earnings:
            net += earn.totalamount
        
        return net
    
    def getexpenses():
        try:
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Expense').all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            earnings = transactionTable.query.filter(transactionTable.userid == current_user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == 'Expense').all()
        net = 0
        for earn in earnings:
            net += earn.totalamount
        
        return net

    def addaccountreceivable(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= startdate).filter(accountsReceivableTable.duedate <= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsReceivableTable.query.filter(accountsReceivableTable.userid == userid).filter(accountsReceivableTable.duedate >= startdate).filter(accountsReceivableTable.duedate <= enddate).all()
        receivables = 0
        for accs in acc:
            receivables += accs.totalamount
        
        return receivables
        
    def addaccountpayable(userid):
        try:
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= startdate).filter(accountsPayableTable.duedate <= enddate).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            user = usersTable.query.filter(usersTable.id == userid).first()
            acc = accountsPayableTable.query.filter(accountsPayableTable.userid == userid).filter(accountsPayableTable.duedate >= startdate).filter(accountsPayableTable.duedate <= enddate).all()
        payables = 0
        for accs in acc:
            payables += accs.totalamount
        
        return payables
    
    def addproperty(userid):
        try:
            props = propertyTable.query.filter(propertyTable.userid == userid).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            props = propertyTable.query.filter(propertyTable.userid == userid).all()
        propvalue = 0
        l_date = date.today()
        for prop in props:
            salvageamount = prop.propertycost * .1
            f_date = prop.propertydate
            delta = l_date - f_date
            diff = delta.days
            years = diff/365
            eol = years/prop.propertylife
            if eol >= 1:
                propvalue = propvalue + (prop.propertycost * .1)
            else:
                salamt = prop.propertycost - salvageamount
                yearlypercentage = 1/prop.propertylife
                yearlydepreciation = salamt * yearlypercentage
                depreciation = yearlydepreciation * years
                propvalue = propvalue + (prop.propertycost - depreciation)
        
        return Decimal(propvalue).quantize(add2)
    

    earns = getearnings()
    accrec = addaccountreceivable(current_user.id)
    accpay = addaccountpayable(current_user.id)
    props = addproperty(current_user.id)
    exp = getexpenses()

    businessname = (user.businessname).upper()
    netearnings = Decimal(earns).quantize(add2)
    netexpenses = Decimal(exp).quantize(add2)
    accountsreceivable = Decimal(accrec).quantize(add2)
    accountspayable = Decimal(accpay).quantize(add2)
    equipment = Decimal(props).quantize(add2)
    totalcashflow = (netearnings + accountsreceivable + equipment) - (accountspayable + netexpenses)

    if form.validate_on_submit():
        return redirect(url_for('cashFlowStatementAdjusted'))


    return render_template('/statements/cash_flow_statement_adjusted.html', datestart = startdate, dateend = enddate,
                           netearnings = "{:,}".format(netearnings), accountsreceivable = "{:,}".format(accountsreceivable),
                           accountspayable = "{:,}".format(accountspayable), netexpenses = "{:,}".format(netexpenses), equipment = "{:,}".format(equipment),
                           totalcashflow = "{:,}".format(totalcashflow), businessname = businessname, form=form)

@app.route('/statements/total_loss_statement', methods=['GET'])
@login_required
def totalLossStatement():
    form = StatementFormRange()

    add2 = Decimal(10) ** -2
    fulldate = date.today()
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Expense").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Expense").all()

    def findadvertising(trans):
        ads = 0
        for tran in trans:
            if tran.transactionreason == "Advertisements":
                ads += tran.totalamount
        return ads
    
    def findmaterialcost(trans):
        mats = 0
        for tran in trans:
            if tran.transactionreason == "Cost of Materials":
                mats += tran.totalamount
        return mats
    
    def findemployeebenefits(trans):
        bens = 0
        for tran in trans:
            if tran.transactionreason == "Employee Benefits":
                bens += tran.totalamount
        return bens
    
    def findinsurance(trans):
        ins = 0
        for tran in trans:
            if tran.transactionreason == "Insurance":
                ins += tran.totalamount
        return ins
    
    def findmaintenance(trans):
        maint = 0
        for tran in trans:
            if tran.transactionreason == "Maintenance":
                maint += tran.totalamount
        return maint
    
    def findofficesupplies(trans):
        supp = 0
        for tran in trans:
            if tran.transactionreason == "Office Supplies":
                supp += tran.totalamount
        return supp
    
    def findpayroll(trans):
        pay = 0
        for tran in trans:
            if tran.transactionreason == "Payroll":
                pay += tran.totalamount
        return pay
    
    def findtravel(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Travel":
                cost += tran.totalamount
        return cost
    
    def findutilities(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Utilities":
                cost += tran.totalamount
        return cost
    
    def findshipping(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Shipping":
                cost += tran.totalamount
        return cost
    
    def findreturns(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Returns":
                cost += tran.totalamount
        return cost
    
    def findother(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Other Expense":
                cost += tran.totalamount
        return cost

    def finddebt():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        ltd = 0
        for debt in debts:
            ltd += debt.debtamount
        
        return ltd
    
    def findinterest():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        interest = 0
        for debt in debts:
            interest += debt.interestpaid
        
        return interest
    
    ads = findadvertising(trans)
    debt = finddebt()
    mats = findmaterialcost(trans)
    benefits = findemployeebenefits(trans)
    ins = findinsurance(trans)
    ints = findinterest()
    maint = findmaintenance(trans)
    offsupp = findofficesupplies(trans)
    pay = findpayroll(trans)
    trav = findtravel(trans)
    util = findutilities(trans)
    ship = findshipping(trans)
    ret = findreturns(trans)
    otherexp = findother(trans)

    startdate = user.fiscalyearstart
    enddate = user.fiscalyearend
    businessname = (user.businessname).upper()
    advertising = Decimal(ads).quantize(add2)
    debt = Decimal(debt).quantize(add2)
    materialcost = Decimal(mats).quantize(add2)
    employeebenefits = Decimal(benefits).quantize(add2)
    insurance = Decimal(ins).quantize(add2)
    interest = Decimal(ints).quantize(add2)
    maintenance = Decimal(maint).quantize(add2)
    officesupplies = Decimal(offsupp).quantize(add2)
    payroll = Decimal(pay).quantize(add2)
    travel = Decimal(trav).quantize(add2)
    utilities = Decimal(util).quantize(add2)
    shipping = Decimal(ship).quantize(add2)
    returns = Decimal(ret).quantize(add2)
    other = Decimal(otherexp).quantize(add2)
    total = advertising + debt + materialcost + employeebenefits + insurance + interest + maintenance + officesupplies + payroll + travel + utilities + shipping + returns + other
    
    

    year = fulldate.year

    if form.validate_on_submit():
        return redirect(url_for('totalLossStatementAdjusted'))

    return render_template('/statements/total_loss_statement.html', year = year, advertising = "{:,}".format(advertising), debt = "{:,}".format(debt), costofmaterials = "{:,}".format(materialcost),
                           employeebenefits = "{:,}".format(employeebenefits), insurance = "{:,}".format(insurance), interestexpense = "{:,}".format(interest),
                           maintenance = "{:,}".format(maintenance), officesupplies = "{:,}".format(officesupplies), payroll = "{:,}".format(payroll),
                           travel = "{:,}".format(travel), utilities = "{:,}".format(utilities), shipping = "{:,}".format(shipping),
                           returns = "{:,}".format(returns), other = "{:,}".format(other), totallosses = "{:,}".format(total), startdate = startdate, enddate = enddate, businessname = businessname,
                           form=form)

@app.route('/statements/total_loss_statement_adjusted', methods=['GET'])
@login_required
def totalLossStatementAdjusted():
    form = StatementFormRange()

    add2 = Decimal(10) ** -2
    startdate = request.args.get('rangestart')
    enddate = request.args.get('rangeend')
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Expense").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Expense").all()

    fulldate = datetime.strptime(enddate, '%Y-%m-%d')

    def findadvertising(trans):
        ads = 0
        for tran in trans:
            if tran.transactionreason == "Advertisements":
                ads += tran.totalamount
        return ads
    
    def findmaterialcost(trans):
        mats = 0
        for tran in trans:
            if tran.transactionreason == "Cost of Materials":
                mats += tran.totalamount
        return mats
    
    def findemployeebenefits(trans):
        bens = 0
        for tran in trans:
            if tran.transactionreason == "Employee Benefits":
                bens += tran.totalamount
        return bens
    
    def findinsurance(trans):
        ins = 0
        for tran in trans:
            if tran.transactionreason == "Insurance":
                ins += tran.totalamount
        return ins
    
    def findmaintenance(trans):
        maint = 0
        for tran in trans:
            if tran.transactionreason == "Maintenance":
                maint += tran.totalamount
        return maint
    
    def findofficesupplies(trans):
        supp = 0
        for tran in trans:
            if tran.transactionreason == "Office Supplies":
                supp += tran.totalamount
        return supp
    
    def findpayroll(trans):
        pay = 0
        for tran in trans:
            if tran.transactionreason == "Payroll":
                pay += tran.totalamount
        return pay
    
    def findtravel(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Travel":
                cost += tran.totalamount
        return cost
    
    def findutilities(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Utilities":
                cost += tran.totalamount
        return cost
    
    def findshipping(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Shipping":
                cost += tran.totalamount
        return cost
    
    def findreturns(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Returns":
                cost += tran.totalamount
        return cost
    
    def findother(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Other Expense":
                cost += tran.totalamount
        return cost

    def finddebt():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        ltd = 0
        for debt in debts:
            ltd += debt.debtamount
        
        return ltd
    
    def findinterest():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        interest = 0
        for debt in debts:
            interest += debt.interestpaid
        
        return interest
    
    ads = findadvertising(trans)
    debt = finddebt()
    mats = findmaterialcost(trans)
    benefits = findemployeebenefits(trans)
    ins = findinsurance(trans)
    ints = findinterest()
    maint = findmaintenance(trans)
    offsupp = findofficesupplies(trans)
    pay = findpayroll(trans)
    trav = findtravel(trans)
    util = findutilities(trans)
    ship = findshipping(trans)
    ret = findreturns(trans)
    otherexp = findother(trans)

    businessname = (user.businessname).upper()
    advertising = Decimal(ads).quantize(add2)
    debt = Decimal(debt).quantize(add2)
    materialcost = Decimal(mats).quantize(add2)
    employeebenefits = Decimal(benefits).quantize(add2)
    insurance = Decimal(ins).quantize(add2)
    interest = Decimal(ints).quantize(add2)
    maintenance = Decimal(maint).quantize(add2)
    officesupplies = Decimal(offsupp).quantize(add2)
    payroll = Decimal(pay).quantize(add2)
    travel = Decimal(trav).quantize(add2)
    utilities = Decimal(util).quantize(add2)
    shipping = Decimal(ship).quantize(add2)
    returns = Decimal(ret).quantize(add2)
    other = Decimal(otherexp).quantize(add2)
    total = advertising + debt + materialcost + employeebenefits + insurance + interest + maintenance + officesupplies + payroll + travel + utilities + shipping + returns + other
    
    

    year = fulldate.year

    if form.validate_on_submit():
        return redirect(url_for('totalLossStatementAdjusted'))

    return render_template('/statements/total_loss_statement_adjusted.html', year = year, advertising = "{:,}".format(advertising), debt = "{:,}".format(debt), costofmaterials = "{:,}".format(materialcost),
                           employeebenefits = "{:,}".format(employeebenefits), insurance = "{:,}".format(insurance), interestexpense = "{:,}".format(interest),
                           maintenance = "{:,}".format(maintenance), officesupplies = "{:,}".format(officesupplies), payroll = "{:,}".format(payroll),
                           travel = "{:,}".format(travel), utilities = "{:,}".format(utilities), shipping = "{:,}".format(shipping),
                           returns = "{:,}".format(returns), other = "{:,}".format(other), totallosses = "{:,}".format(total), startdate = startdate, enddate = enddate, businessname = businessname,
                           form=form)

@app.route('/statements/profit_loss_statements', methods=['GET'])
@login_required
def profitLossStatement():
    form = StatementFormRange()

    add2 = Decimal(10) ** -2
    fulldate = date.today()
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Expense").all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Income").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Expense").all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Income").all()

    def findadvertising(trans):
        ads = 0
        for tran in trans:
            if tran.transactionreason == "Advertisements":
                ads += tran.totalamount
        return ads
    
    def findmaterialcost(trans):
        mats = 0
        for tran in trans:
            if tran.transactionreason == "Cost of Materials":
                mats += tran.totalamount
        return mats
    
    def findemployeebenefits(trans):
        bens = 0
        for tran in trans:
            if tran.transactionreason == "Employee Benefits":
                bens += tran.totalamount
        return bens
    
    def findinsurance(trans):
        ins = 0
        for tran in trans:
            if tran.transactionreason == "Insurance":
                ins += tran.totalamount
        return ins
    
    def findmaintenance(trans):
        maint = 0
        for tran in trans:
            if tran.transactionreason == "Maintenance":
                maint += tran.totalamount
        return maint
    
    def findofficesupplies(trans):
        supp = 0
        for tran in trans:
            if tran.transactionreason == "Office Supplies":
                supp += tran.totalamount
        return supp
    
    def findpayroll(trans):
        pay = 0
        for tran in trans:
            if tran.transactionreason == "Payroll":
                pay += tran.totalamount
        return pay
    
    def findtravel(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Travel":
                cost += tran.totalamount
        return cost
    
    def findutilities(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Utilities":
                cost += tran.totalamount
        return cost
    
    def findshipping(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Shipping":
                cost += tran.totalamount
        return cost
    
    def findreturns(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Returns":
                cost += tran.totalamount
        return cost
    
    def findother(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Other Expense":
                cost += tran.totalamount
        return cost

    def finddebt():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        ltd = 0
        for debt in debts:
            ltd += debt.debtamount
        
        return ltd
    
    def findinterest():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        interest = 0
        for debt in debts:
            interest += debt.interestpaid
        
        return interest

    def findsales(transinc):
        inc = 0
        for tran in transinc:
            if tran.transactionreason == "Sales":
                inc += tran.totalamount
        return inc
    
    def findservice(transinc):
        inc = 0
        for tran in transinc:
            if tran.transactionreason == "Services":
                inc += tran.totalamount
        return inc
    
    def findotherincome(transinc):
        inc = 0
        for tran in transinc:
            if tran.transactionreason == "Other Income":
                inc += tran.totalamount
        return inc
    
    def posorneg(profitloss):
        if profitloss >= 0:
            profloss = True
        elif profitloss < 0:
            profloss = False
        
        return profloss
    
    def findclass(pro):
        if pro:
            classchange = "text-success"
        elif not pro:
            classchange = "text-danger"
        
        return classchange

    ads = findadvertising(trans)
    debt = finddebt()
    mats = findmaterialcost(trans)
    benefits = findemployeebenefits(trans)
    ins = findinsurance(trans)
    ints = findinterest()
    maint = findmaintenance(trans)
    offsupp = findofficesupplies(trans)
    pay = findpayroll(trans)
    trav = findtravel(trans)
    util = findutilities(trans)
    ship = findshipping(trans)
    ret = findreturns(trans)
    otherexp = findother(trans)
    sale = findsales(transinc)
    serv = findservice(transinc)
    othinc = findotherincome(transinc)

    startdate = user.fiscalyearstart
    enddate = user.fiscalyearend
    businessname = (user.businessname).upper()
    sales = Decimal(sale).quantize(add2)
    service = Decimal(serv).quantize(add2)
    otherincome = Decimal(othinc).quantize(add2)
    totalprofit = sales + service + otherincome
    advertising = Decimal(ads).quantize(add2)
    debt = Decimal(debt).quantize(add2)
    materialcost = Decimal(mats).quantize(add2)
    employeebenefits = Decimal(benefits).quantize(add2)
    insurance = Decimal(ins).quantize(add2)
    interest = Decimal(ints).quantize(add2)
    maintenance = Decimal(maint).quantize(add2)
    officesupplies = Decimal(offsupp).quantize(add2)
    payroll = Decimal(pay).quantize(add2)
    travel = Decimal(trav).quantize(add2)
    utilities = Decimal(util).quantize(add2)
    shipping = Decimal(ship).quantize(add2)
    returns = Decimal(ret).quantize(add2)
    other = Decimal(otherexp).quantize(add2)
    total = advertising + debt + materialcost + employeebenefits + insurance + interest + maintenance + officesupplies + payroll + travel + utilities + shipping + returns + other

    profloss = totalprofit - total

    diff = Decimal(profloss).quantize(add2)
    profitloss = "{:,}".format(diff)

    classbool = posorneg(diff)
    classchange = findclass(classbool)

    year = fulldate.year

    if form.validate_on_submit():
        return redirect(url_for('profitLossStatementAdjusted'))
    
    return render_template('/statements/profit_loss_statement.html', year = year, advertising = "{:,}".format(advertising), debt = "{:,}".format(debt), costofmaterials = "{:,}".format(materialcost),
                           employeebenefits = "{:,}".format(employeebenefits), insurance = "{:,}".format(insurance), interestexpense = "{:,}".format(interest),
                           maintenance = "{:,}".format(maintenance), officesupplies = "{:,}".format(officesupplies), payroll = "{:,}".format(payroll),
                           travel = "{:,}".format(travel), utilities = "{:,}".format(utilities), shipping = "{:,}".format(shipping),
                           returns = "{:,}".format(returns), other = "{:,}".format(other), totallosses = "{:,}".format(total), startdate = startdate, enddate = enddate, businessname = businessname,
                           sales = "{:,}".format(sales), service = "{:,}".format(service), otherincome = "{:,}".format(otherincome), totalprofit = "{:,}".format(totalprofit), profitloss = profitloss, classchange = classchange,
                           form = form)

@app.route('/statements/profit_loss_statement_adjusted', methods=['GET'])
@login_required
def profitLossStatementAdjusted():
    form = StatementFormRange()

    startdate = request.args.get('rangestart')
    enddate = request.args.get('rangeend')

    add2 = Decimal(10) ** -2
    fulldate = date.today()
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Expense").all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Income").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Expense").all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Income").all()

    def findadvertising(trans):
        ads = 0
        for tran in trans:
            if tran.transactionreason == "Advertisements":
                ads += tran.totalamount
        return ads
    
    def findmaterialcost(trans):
        mats = 0
        for tran in trans:
            if tran.transactionreason == "Cost of Materials":
                mats += tran.totalamount
        return mats
    
    def findemployeebenefits(trans):
        bens = 0
        for tran in trans:
            if tran.transactionreason == "Employee Benefits":
                bens += tran.totalamount
        return bens
    
    def findinsurance(trans):
        ins = 0
        for tran in trans:
            if tran.transactionreason == "Insurance":
                ins += tran.totalamount
        return ins
    
    def findmaintenance(trans):
        maint = 0
        for tran in trans:
            if tran.transactionreason == "Maintenance":
                maint += tran.totalamount
        return maint
    
    def findofficesupplies(trans):
        supp = 0
        for tran in trans:
            if tran.transactionreason == "Office Supplies":
                supp += tran.totalamount
        return supp
    
    def findpayroll(trans):
        pay = 0
        for tran in trans:
            if tran.transactionreason == "Payroll":
                pay += tran.totalamount
        return pay
    
    def findtravel(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Travel":
                cost += tran.totalamount
        return cost
    
    def findutilities(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Utilities":
                cost += tran.totalamount
        return cost
    
    def findshipping(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Shipping":
                cost += tran.totalamount
        return cost
    
    def findreturns(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Returns":
                cost += tran.totalamount
        return cost
    
    def findother(trans):
        cost = 0
        for tran in trans:
            if tran.transactionreason == "Other Expense":
                cost += tran.totalamount
        return cost

    def finddebt():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        ltd = 0
        for debt in debts:
            ltd += debt.debtamount
        
        return ltd
    
    def findinterest():
        try:
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        except(AttributeError, SQLAlchemy.exc.OperationalError):
            debts = debtTable.query.filter(debtTable.userid == user.id).filter(debtTable.debtamount > 0).all()
        interest = 0
        for debt in debts:
            interest += debt.interestpaid
        
        return interest

    def findsales(transinc):
        inc = 0
        for tran in transinc:
            if tran.transactionreason == "Sales":
                inc += tran.totalamount
        return inc
    
    def findservice(transinc):
        inc = 0
        for tran in transinc:
            if tran.transactionreason == "Services":
                inc += tran.totalamount
        return inc
    
    def findotherincome(transinc):
        inc = 0
        for tran in transinc:
            if tran.transactionreason == "Other Income":
                inc += tran.totalamount
        return inc
    
    def posorneg(profitloss):
        if profitloss >= 0:
            profloss = True
        elif profitloss < 0:
            profloss = False
        
        return profloss
    
    def findclass(pro):
        if pro:
            classchange = "text-success"
        elif not pro:
            classchange = "text-danger"
        
        return classchange

    ads = findadvertising(trans)
    debt = finddebt()
    mats = findmaterialcost(trans)
    benefits = findemployeebenefits(trans)
    ins = findinsurance(trans)
    ints = findinterest()
    maint = findmaintenance(trans)
    offsupp = findofficesupplies(trans)
    pay = findpayroll(trans)
    trav = findtravel(trans)
    util = findutilities(trans)
    ship = findshipping(trans)
    ret = findreturns(trans)
    otherexp = findother(trans)
    sale = findsales(transinc)
    serv = findservice(transinc)
    othinc = findotherincome(transinc)

    businessname = (user.businessname).upper()
    sales = Decimal(sale).quantize(add2)
    service = Decimal(serv).quantize(add2)
    otherincome = Decimal(othinc).quantize(add2)
    totalprofit = sales + service + otherincome
    advertising = Decimal(ads).quantize(add2)
    debt = Decimal(debt).quantize(add2)
    materialcost = Decimal(mats).quantize(add2)
    employeebenefits = Decimal(benefits).quantize(add2)
    insurance = Decimal(ins).quantize(add2)
    interest = Decimal(ints).quantize(add2)
    maintenance = Decimal(maint).quantize(add2)
    officesupplies = Decimal(offsupp).quantize(add2)
    payroll = Decimal(pay).quantize(add2)
    travel = Decimal(trav).quantize(add2)
    utilities = Decimal(util).quantize(add2)
    shipping = Decimal(ship).quantize(add2)
    returns = Decimal(ret).quantize(add2)
    other = Decimal(otherexp).quantize(add2)
    total = advertising + debt + materialcost + employeebenefits + insurance + interest + maintenance + officesupplies + payroll + travel + utilities + shipping + returns + other

    profloss = totalprofit - total

    diff = Decimal(profloss).quantize(add2)
    profitloss = "{:,}".format(diff)

    classbool = posorneg(diff)
    classchange = findclass(classbool)

    year = fulldate.year

    if form.validate_on_submit():
        return redirect(url_for('profitLossStatementAdjusted'))
    
    return render_template('/statements/profit_loss_statement_adjusted.html', year = year, advertising = "{:,}".format(advertising), debt = "{:,}".format(debt), costofmaterials = "{:,}".format(materialcost),
                           employeebenefits = "{:,}".format(employeebenefits), insurance = "{:,}".format(insurance), interestexpense = "{:,}".format(interest),
                           maintenance = "{:,}".format(maintenance), officesupplies = "{:,}".format(officesupplies), payroll = "{:,}".format(payroll),
                           travel = "{:,}".format(travel), utilities = "{:,}".format(utilities), shipping = "{:,}".format(shipping),
                           returns = "{:,}".format(returns), other = "{:,}".format(other), totallosses = "{:,}".format(total), startdate = startdate, enddate = enddate, businessname = businessname,
                           sales = "{:,}".format(sales), service = "{:,}".format(service), otherincome = "{:,}".format(otherincome), totalprofit = "{:,}".format(totalprofit), profitloss = profitloss, classchange = classchange,
                           form = form)

@app.route('/statements/equity_statement', methods=['GET'])
@login_required
def equityStatement():
    form = StatementFormRange()

    add2 = Decimal(10) ** -2
    fulldate = date.today()
    year = fulldate.year
    lastyearfull = date.today() - timedelta(days=365)
    lastyear = lastyearfull.year
    try:
        user = usersTable.query.filter(usersTable.id == current_user.id).first()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        user = usersTable.query.filter(usersTable.id == current_user.id).first()

    laststart = user.fiscalyearstart - relativedelta(years = 1)
    lastend = user.fiscalyearend - relativedelta(years = 1)

    try:
        invs = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= user.fiscalyearstart).filter(investmentTable.investmentdate <= user.fiscalyearend).all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Income").all()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Expense").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        invs = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= user.fiscalyearstart).filter(investmentTable.investmentdate <= user.fiscalyearend).all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Income").all()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= user.fiscalyearstart).filter(transactionTable.transactiondate <= user.fiscalyearend).filter(transactionTable.transactiontype == "Expense").all()

    try:
        invslast = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= laststart).filter(investmentTable.investmentdate <= lastend).all()
        transinclast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Income").all()
        translast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Expense").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        invslast = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= laststart).filter(investmentTable.investmentdate <= lastend).all()
        transinclast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Income").all()
        translast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Expense").all()

    def findinvestments(invs):
        total = 0
        for inv in invs:
            total += inv.investmentamount
        
        return total
    
    def findincome(transinc):
        total = 0
        for tran in transinc:
            total += tran.totalamount
        
        return total
    
    def findlosses(trans):
        total = 0
        for tran in trans:
            total += tran.totalamount
        
        return total

    lastinv = findinvestments(invslast)
    lastinc = findincome(transinclast)
    lastloss = findlosses(translast)
    caplast = (lastinv + lastinc) - lastloss
    totalcaplast = Decimal(caplast).quantize(add2)
    
    inv = findinvestments(invs)
    inc = findincome(transinc)
    loss = findlosses(trans)
    total = (inv + inc) - loss

    investments = Decimal(inv).quantize(add2)
    income = Decimal(inc).quantize(add2)
    losses = Decimal(loss).quantize(add2)
    totalcap = Decimal(total).quantize(add2)
    totalcapital = totalcap + totalcaplast

    if form.validate_on_submit():
        return redirect(url_for('equityStatementAdjusted'))

    return render_template('/statements/equity_statement.html', currentyear = year, lastyear = lastyear, startdate = user.fiscalyearstart, enddate = user.fiscalyearend, businessname = user.businessname,
                           investments = "{:,}".format(investments), income = "{:,}".format(income), losses = "{:,}".format(losses), totalcapital = "{:,}".format(totalcapital), lastyearcapital = "{:,}".format(totalcaplast),
                           form=form)

@app.route('/statements/equity_statement_adjusted', methods=['GET'])
@login_required
def equityStatementAdjusted():
    form = StatementFormRange()

    startdate = request.args.get('rangestart')
    enddate = request.args.get('rangeend')

    newstart = startdate
    newend = startdate

    startdate = datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.strptime(enddate, '%Y-%m-%d')

    add2 = Decimal(10) ** -2
    laststart = startdate - relativedelta(years=1)
    lastend = enddate - relativedelta(years=1)
    lastyearstart = laststart.date()
    lastyearend = lastend.date()
    user = usersTable.query.filter(usersTable.id == current_user.id).first()

    laststart = startdate - relativedelta(years = 1)
    lastend = enddate - relativedelta(years = 1)

    try:
        invs = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= startdate).filter(investmentTable.investmentdate <= enddate).all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Income").all()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Expense").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        invs = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= startdate).filter(investmentTable.investmentdate <= enddate).all()
        transinc = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Income").all()
        trans = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= startdate).filter(transactionTable.transactiondate <= enddate).filter(transactionTable.transactiontype == "Expense").all()

    try:
        invslast = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= laststart).filter(investmentTable.investmentdate <= lastend).all()
        transinclast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Income").all()
        translast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Expense").all()
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        invslast = investmentTable.query.filter(investmentTable.userid == current_user.id).filter(investmentTable.investmentdate >= laststart).filter(investmentTable.investmentdate <= lastend).all()
        transinclast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Income").all()
        translast = transactionTable.query.filter(transactionTable.userid == user.id).filter(transactionTable.transactiondate >= laststart).filter(transactionTable.transactiondate <= lastend).filter(transactionTable.transactiontype == "Expense").all()

    def findinvestments(invs):
        total = 0
        for inv in invs:
            total += inv.investmentamount
        
        return total
    
    def findincome(transinc):
        total = 0
        for tran in transinc:
            total += tran.totalamount
        
        return total
    
    def findlosses(trans):
        total = 0
        for tran in trans:
            total += tran.totalamount
        
        return total

    lastinv = findinvestments(invslast)
    lastinc = findincome(transinclast)
    lastloss = findlosses(translast)
    caplast = (lastinv + lastinc) - lastloss
    totalcaplast = Decimal(caplast).quantize(add2)
    
    inv = findinvestments(invs)
    inc = findincome(transinc)
    loss = findlosses(trans)
    total = (inv + inc) - loss

    investments = Decimal(inv).quantize(add2)
    income = Decimal(inc).quantize(add2)
    losses = Decimal(loss).quantize(add2)
    totalcap = Decimal(total).quantize(add2)
    totalcapital = totalcap + totalcaplast

    if form.validate_on_submit():
        return redirect(url_for('equityStatementAdjusted'))

    return render_template('/statements/equity_statement_adjusted.html', startdate = newstart, enddate = newend, businessname = user.businessname, laststart = lastyearstart, lastend = lastyearend,
                           investments = "{:,}".format(investments), income = "{:,}".format(income), losses = "{:,}".format(losses), totalcapital = "{:,}".format(totalcapital), lastyearcapital = "{:,}".format(totalcaplast),
                           form=form)

@app.route('/statements/chart_of_accounts', methods=['GET'])
@login_required
def chartOfAccountsStatement():
    try:
        accounts = accountTable.query.filter(accountTable.userid==current_user.id).order_by(asc(accountTable.accountnumber))
    except(AttributeError, SQLAlchemy.exc.OperationalError):
        accounts = accountTable.query.filter(accountTable.userid==current_user.id).order_by(asc(accountTable.accountnumber))

    return render_template('statements/chart_of_accounts.html', rows=accounts)