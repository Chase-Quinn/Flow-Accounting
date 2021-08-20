from flask_table import Table, Col
from datetime import date, timedelta, datetime

class AccountResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'AccountResults'
    
    accountid = Col('AId', show=False)
    userid = Col('UId', show=False)
    accountnumber = Col('Account')
    mainname = Col('Main Name', show=False)
    accountname = Col('Name')
    accountdescription = Col('Description')
    accountdate = Col('Date')
    main = Col('Main', show=False)

class TransactionResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'TransactionResults'

    accountid = Col("Account")
    userid = Col("UId", show=False)
    transactionid = Col("Id")
    transactiontype = Col("Type")
    transactionmethod = Col("Method")
    transactionsource = Col("Source")
    pretaxtotal = Col("Pre-Tax Total", show=False)
    transactiondescription = Col("Desc")
    salestax = Col("Tax", show=False)
    totalamount = Col("Total")
    transactionreason = Col("Reason")
    transactiondate = Col("Date")

class DebtResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'AccountResults'

    userid = Col("UId", show=False)
    debtid = Col("ID", show=False)
    accountnumber = Col("Account")
    debtvendor = Col("Vendor")
    debtamount = Col("Current Amount")
    debtapr = Col("APR %")
    debtdescription = Col("Description")
    debtdate = Col("Date")
    interestpaid = Col("Interest Paid")

class InvestmentResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'AccountResults'

    userid = Col("UId", show=False)
    investmentid = Col("ID", show=False)
    accountnumber = Col("Account")
    fname = Col("First Name")
    lname = Col("Last Name")
    investmentamount = Col("Amount")
    investmentdescription = Col("Description")
    investmentdate = Col("Date")

class CustomerResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'AccountResults'

    customerid = Col("CId", show=False)
    userid = Col("UId", show=False)
    accountnumber = Col("Account")
    customername = Col("Customer")
    customerdescription = Col("Description")
    customerdate = Col("Date")

class VendorResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'AccountResults'

    vendorid = Col("VId", show=False)
    userid = Col("UId", show=False)
    accountnumber = Col("Account")
    vendorname = Col("Vendor")
    vendordescription = Col("Description")
    vendordate = Col("Date")

class TransactionLog(Table):
    classes = ['table', 'col-12', 'h-90', 'text-left']
    table_id = 'TransactionLog'

    accountid = Col("Account")
    userid = Col("UId", show=False)
    transactionid = Col("Id")
    transactiontype = Col("Type")
    transactionmethod = Col("Method")
    transactionsource = Col("Source")
    pretaxtotal = Col("Pre-Tax Total", show=False)
    transactiondescription = Col("Desc")
    salestax = Col("Tax", show=False)
    totalamount = Col("Total")
    transactionreason = Col("Reason")
    transactiondate = Col("Date")

class AccountLog(Table):
    classes = ['table', 'col-12', 'text-left']
    table_id = 'AccountLog'
    
    accountid = Col('AId', show=False)
    userid = Col('UId', show=False)
    accountnumber = Col('Account')
    mainname = Col('Main Name', show=False)
    accountname = Col('Name')
    accountdescription = Col('Description')
    accountdate = Col('Date')
    main = Col('Main', show=False)

class PropertyResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    
    userid = Col("CId", show=False)
    propertyid = Col("ID")
    propertyname = Col("Name")
    propertydescription = Col("Description")
    propertycost = Col("Cost")
    propertydate = Col("Date")
    propertylife = Col("Life", show=False)

class RecPayResults(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'RecPayResults'

    accountid = Col("Account")
    userid = Col("UId", show=False)
    transactionid = Col("Id")
    transactiontype = Col("Type", show=False)
    transactionmethod = Col("Method")
    transactionsource = Col("Source")
    pretaxtotal = Col("Pre-Tax Total", show=False)
    transactiondescription = Col("Desc / P.O. #")
    salestax = Col("Tax", show=False)
    totalamount = Col("Total")
    transactionreason = Col("Reason")
    duedate = Col("Due Date", td_html_attrs = {'class': 'duedate'})

class BalanceTable(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'BalanceResults'

    userid = Col("UId", show=False)
    balanceid = Col("BId", show=False)
    bankname = Col("Bank Name")
    bankbalance = Col("Balance", td_html_attrs = {'class': 'bankbalance'})
    date = Col("Recorded Date")

class LossesTable(Table):
    classes = ['table', 'table-scroll', 'bg-dark', 'table-dark', 'col-12', 'h-90', 'text-left']
    table_id = 'BalanceResults'

    userid = Col("UId", show=False)
    lossid = Col("LId", show=False)
    lossdescription = Col("Description")
    lossamount = Col("Amount")
    lossreason = Col("Reason")
    lossdate = Col("Date")