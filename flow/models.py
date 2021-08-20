from flask_sqlalchemy import SQLAlchemy
from flow import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(userid):
    return usersTable.query.get(userid)

class usersTable(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    joined = db.Column(db.Date, nullable=False)
    businessname = db.Column(db.String(255), nullable=False)
    businessnumber = db.Column(db.String(255), nullable=False)
    businessaddress = db.Column(db.String(255), nullable=False)
    businesscity = db.Column(db.String(255), nullable=False)
    businessstate = db.Column(db.String(50))
    businesszip = db.Column(db.Integer)
    businesswebsite = db.Column(db.String(255))
    fiscalyearstart = db.Column(db.Date, nullable=False)
    fiscalyearend = db.Column(db.Date, nullable=False)
    businesslogo = db.Column(db.String(255), nullable=False)
    member = db.Column(db.Boolean, nullable = False)
    lastpaydate = db.Column(db.Date)
    subuser = db.relationship('subuserTable', backref='user', lazy=True)
    account = db.relationship('accountTable', backref='user', lazy=True)
    vendor = db.relationship('vendorTable', backref='user', lazy=True)
    customer = db.relationship('customerTable', backref='user', lazy=True)
    debt = db.relationship('debtTable', backref='user', lazy=True)
    investment = db.relationship('investmentTable', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=900):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return usersTable.query.get(user_id)

class subuserTable(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    subid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)

class accountTable(db.Model):
    accountid = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    accountnumber = db.Column(db.Integer, nullable=False)
    accountname = db.Column(db.String(255), nullable=False)
    accountdescription = db.Column(db.String(255), nullable=False)
    accountdate = db.Column(db.Date, nullable=False)
    main = db.Column(db.Boolean, nullable=False)
    mainname = db.Column(db.String(255), nullable=False)

class transactionTable(db.Model):
    accountid = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer,nullable=False)
    transactionid = db.Column(db.Integer, primary_key=True, nullable=False)
    transactiontype = db.Column(db.String(255), nullable=False)
    transactionsource = db.Column(db.String(255), nullable=False)
    transactionmethod = db.Column(db.String(255), nullable=False)
    pretaxtotal = db.Column(db.Float)
    transactiondescription = db.Column(db.String(255), nullable=False)
    salestax = db.Column(db.Float, nullable=False)
    totalamount = db.Column(db.Float)
    transactiondate = db.Column(db.Date, nullable=False)
    transactionreason = db.Column(db.String(255), nullable=False)

class vendorTable(db.Model):
    vendorid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    accountnumber = db.Column(db.Integer, nullable=False)
    vendorname = db.Column(db.String(255), nullable=False)
    vendordescription = db.Column(db.String(255), nullable=False)
    vendordate = db.Column(db.Date, nullable=False)

class customerTable(db.Model):
    customerid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    accountnumber = db.Column(db.Integer, nullable=False)
    customername = db.Column(db.String(255), nullable=False)
    customerdescription = db.Column(db.String(255), nullable=False)
    customeremail = db.Column(db.String(255))
    customernumber = db.Column(db.String(255))
    customeraddress = db.Column(db.String(255))
    customercity = db.Column(db.String(255))
    customerstate = db.Column(db.String(255))
    customerzip = db.Column(db.Integer)
    customerdate = db.Column(db.Date, nullable=False)

class investmentTable(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    accountnumber = db.Column(db.Integer, nullable=False)
    investmentid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    investmentamount = db.Column(db.Float, nullable=False)
    investmentdescription = db.Column(db.String(255), nullable=False)
    investmentdate = db.Column(db.Date, nullable=False)

class debtTable(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    debtid= db.Column(db.Integer, primary_key=True)
    accountnumber = db.Column(db.Integer, nullable=False)
    debtvendor = db.Column(db.String(255), nullable=False)
    debtamount = db.Column(db.Float, nullable=False)
    debtapr = db.Column(db.Float, nullable=False)
    debtdescription = db.Column(db.String(255), nullable=False)
    debtdate = db.Column(db.Date, nullable=False)
    interestpaid = db.Column(db.Float, nullable = False)

class feedbackTable(db.Model):
    userid = db.Column(db.Integer, nullable=False, primary_key=True)
    feedback = db.Column(db.String(255), nullable=False)
    feedbackdate = db.Column(db.Date, nullable = False)

class bugReportTable(db.Model):
    userid = db.Column(db.Integer, nullable=False, primary_key=True)
    bugtype = db.Column(db.String(255), nullable=False)
    bugdescription = db.Column(db.String(255), nullable=False)
    bugdate = db.Column(db.Date, nullable=False)

class bankTable(db.Model):
    userid = db.Column(db.Integer, nullable=False, primary_key=True)
    accountnumber = db.Column(db.Integer, nullable=False)
    bankname = db.Column(db.String(255), nullable=False)
    bankbalance = db.Column(db.Float, nullable=False)
    bankdate = db.Column(db.Date, nullable=False)

class propertyTable(db.Model):
    userid = db.Column(db.Integer, nullable=False)
    propertyid = db.Column(db.Integer, nullable=False, primary_key=True)
    propertyname = db.Column(db.String(255), nullable=False)
    propertycost = db.Column(db.Float, nullable=False)
    propertydescription = db.Column(db.String(255), nullable=False)
    propertydate = db.Column(db.Date, nullable=False)
    propertylife = db.Column(db.Integer, nullable=False)

class accountsPayableTable(db.Model):
    accountid = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer,nullable=False)
    transactionid = db.Column(db.Integer, primary_key=True, nullable=False)
    transactiontype = db.Column(db.String(255), nullable=False)
    transactionsource = db.Column(db.String(255), nullable=False)
    transactionmethod = db.Column(db.String(255), nullable=False)
    pretaxtotal = db.Column(db.Float)
    transactiondescription = db.Column(db.String(255), nullable=False)
    salestax = db.Column(db.Float, nullable=False)
    totalamount = db.Column(db.Float)
    duedate = db.Column(db.Date, nullable=False)
    transactionreason = db.Column(db.String(255), nullable=False)

class accountsReceivableTable(db.Model):
    accountid = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer,nullable=False)
    transactionid = db.Column(db.Integer, primary_key=True, nullable=False)
    transactiontype = db.Column(db.String(255), nullable=False)
    transactionsource = db.Column(db.String(255), nullable=False)
    transactionmethod = db.Column(db.String(255), nullable=False)
    pretaxtotal = db.Column(db.Float)
    transactiondescription = db.Column(db.String(255), nullable=False)
    salestax = db.Column(db.Float, nullable=False)
    totalamount = db.Column(db.Float)
    duedate = db.Column(db.Date, nullable=False)
    transactionreason = db.Column(db.String(255), nullable=False)
    paid = db.Column(db.Boolean, nullable=False)
    invoicenumber = db.Column(db.Integer)

class balanceTable(db.Model):
    userid = db.Column(db.Integer, nullable=False)
    balanceid = db.Column(db.Integer, nullable=False, primary_key=True)
    bankname = db.Column(db.String(254), nullable=False)
    bankbalance = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class emailList(db.Model):
    email = db.Column(db.String(255), primary_key=True, nullable=False)

# class invoices(db.Model):
#     userid = db.Column(db.Integer, nullable=False)
#     invoiceid = db.Column(db.Integer, nullable=False, primary_key=True)
#     invoicenumber = db.Column(db.Integer, nullable=False)
#     customer = db.Column(db.String(255), nullable=False)
#     customeremail = db.Column(db.String(255), nullable=False)
#     billingaddress = db.Column(db.String(255), nullable = False)
#     billingstate = db.Column(db.String(255), nullable=False)
#     billingcity = db.Column(db.String(255), nullable=False)
#     billingzip = db.Column(db.Integer, nullable=False)
#     term = db.Column(db.Integer, nullable = False)
#     date = db.Column(db.Date, nullable = False)
#     duedate = db.Column(db.Date, nullable = False)
#     paid = db.Column(db.Boolean, nullable=False)