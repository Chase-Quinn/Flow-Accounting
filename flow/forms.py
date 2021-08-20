from wtforms.fields.html5 import DateField
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, FileField, SelectField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from flow import app, bootstrap, db
from flow.models import *

class NoLabelMixin(object):
    def __init__(self, *args, **kwargs):
        super(NoLabelMixin, self).__init__(*args, **kwargs)
        for field_name in self._fields:
            field_property = getattr(self, field_name)
            field_property.label = None

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class SignupForm(FlaskForm):
    firstname = StringField('*First Name', validators=[InputRequired(), Length(min=2, max=30)])
    lastname = StringField('*Last Name', validators=[InputRequired(), Length(min=2, max=30)])
    username = StringField('*Username', validators=[InputRequired(), Length(min=4, max=40)])
    password = PasswordField('*Password', validators=[InputRequired(), EqualTo('validatepassword', message='Your passwords did not match.'), Length(min=8, max=80)])
    validatepassword = PasswordField('*Validate Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('*Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=120)])
    businessname = StringField('*Business Name', validators=[InputRequired()])
    businessaddress = StringField('*Business Address', validators=[InputRequired()])
    businessstate = SelectField('*State', choices=[('AL', 'AL'), ('AK', 'AK'), ('AR', 'AR'), ('AZ', 'AZ'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('IA', 'IA'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('MA', 'MA'), ('MD', 'MD'), ('ME', 'ME'), ('MI', 'MI'), ('MN', 'MN'), ('MO', 'MO'), ('MS', 'MS'), ('MT', 'MT'), ('NC', 'NC'), ('NE', 'NE'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NV', 'NV'), ('NY', 'NY'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WI', 'WI'), ('WV', 'WV'), ('WY', 'WY'), ('AS', '*AS'), ('GU', '*GU'), ('MP', '*MP'), ('PR', '*PR'), ('UM', '*UM'), ('VI', '*VI'), ('AA', '*AA'), ('AP', '*AP'), ('AE', '*AE')], validators=[InputRequired()])
    businesscity = StringField('*City', validators=[InputRequired()])
    businesszip = IntegerField('*Zipcode', validators=[InputRequired()])
    businesswebsite = StringField('Business Website')
    fiscalyearstart = DateField('*Fiscal Year Start', validators=[InputRequired()])
    fiscalyearend = DateField('*Fiscal Year End', validators=[InputRequired()])
    businesslogo = FileField('Business Logo', default='default_logo.png', validators=[FileAllowed(['jpg', 'png'])])
    bankname = StringField('*Bank Account Name', validators=[InputRequired()])
    bankbalance = FloatField('*Starting Balance', validators=[InputRequired()])

    def validate_username(self, username):
        username = usersTable.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError('That username is already taken.')

    def validate_email(self, email):
        email = usersTable.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already registered with an account.')
    
class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=40)])

    def validate_email(self, email):
        if email.data != current_user.email:
            email = usersTable.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That is email is already registered with another account.')
        elif email.data == current_user.email:
            raise ValidationError('That is your registered email.')
            
class AccountForm(FlaskForm):
    accountnumber = IntegerField('Account Number', validators=[InputRequired()])
    accountname = StringField('Account Name', validators=[InputRequired(), Length(max=20)])
    description = StringField('Description', validators=[InputRequired(), Length(max=20)])
    date = DateField('Account Date', validators=[InputRequired()])

class CustomerForm(FlaskForm):
    accountsignature = SelectField('Account', choices=[], validators=[InputRequired()])
    customername = StringField('Customer Name', validators=[InputRequired(), Length(max=40)])
    description = StringField('Description', validators=[InputRequired(), Length(max=30)])
    email = StringField('*Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=120)])
    address = StringField('Address', validators=[InputRequired(), Length(max=30)])
    city = StringField('City', validators=[InputRequired(), Length(max=30)])
    state = SelectField('State', choices=[('AL', 'AL'), ('AK', 'AK'), ('AR', 'AR'), ('AZ', 'AZ'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('IA', 'IA'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('MA', 'MA'), ('MD', 'MD'), ('ME', 'ME'), ('MI', 'MI'), ('MN', 'MN'), ('MO', 'MO'), ('MS', 'MS'), ('MT', 'MT'), ('NC', 'NC'), ('NE', 'NE'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NV', 'NV'), ('NY', 'NY'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WI', 'WI'), ('WV', 'WV'), ('WY', 'WY'), ('AS', '*AS'), ('GU', '*GU'), ('MP', '*MP'), ('PR', '*PR'), ('UM', '*UM'), ('VI', '*VI'), ('AA', '*AA'), ('AP', '*AP'), ('AE', '*AE')], validators=[InputRequired()])
    zip = IntegerField('Zip Code', validators=[InputRequired(), NumberRange(max = 99999)])
    number = StringField('Phone Number', validators=[InputRequired(), Length(max=30)])

class VendorForm(FlaskForm):
    accountsignature = SelectField('Account', choices=[], validators=[InputRequired()])
    vendorname = StringField('Vendor Name', validators=[InputRequired(), Length(max=40)])
    description = StringField('Description', validators=[InputRequired(), Length(max=30)])

class InvestmentForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    amount = FloatField('Amount', validators=[InputRequired()])
    method = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired(), Length(max=25)])
    date = DateField('Investment Date', validators=[InputRequired()])

class TransactionIncomeForm(FlaskForm):
    transactionsource = SelectField('Customer', choices=[], coerce=int)
    transactiondescription = StringField('Description', validators=[InputRequired()])
    pretaxtotal = FloatField('Pre-Tax Total', validators=[InputRequired()])
    salestax = FloatField('Sales Tax *only if there is sales tax', default=0, validators=[InputRequired()])
    totalamount = FloatField('Total Amount', render_kw={'readonly': True}, validators=[InputRequired()])
    transactionmethod = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    transactiondate = DateField('Date', validators=[InputRequired()])
    transactionreason = SelectField('Reason', choices=[('Sales', 'Sales'), ('Services', 'Services'), ('Other Income', 'Other Income')] , validators=[InputRequired()])

class TransactionExpenseForm(FlaskForm):
    transactionsource = SelectField('Vendor', choices=[], coerce=int)
    transactiondescription = StringField('Description', validators=[InputRequired()])
    pretaxtotal = FloatField('Pre-Tax Total', validators=[InputRequired()])
    salestax = FloatField('Sales Tax *only if there is sales tax', default=0, validators=[InputRequired()])
    totalamount = FloatField('Total Amount', render_kw={'readonly': True}, validators=[InputRequired()])
    transactionmethod = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    transactiondate = DateField('Date', validators=[InputRequired()])
    transactionreason = SelectField('Reason', choices=[('Payroll', 'Payroll'), ('Utilities', 'Utilities'), ('Advertisements', 'Advertisements'), ('Cost of Materials', 'Cost of Materials'), ('Employee Benefits', 'Employee Benefits'), ('Insurance', 'Insurance'), ('Maintenance', 'Maintenance'), ('Office Supplies', 'Office Supplies'), ('Travel', 'Travel'), ('Shipping', 'Shipping'), ('Returns', 'Returns'), ('Other Expense', 'Other Expense')] , validators=[InputRequired()])

class DebtForm(FlaskForm):
    vendorname = SelectField('Vendor', choices=[], validators=[InputRequired()])
    amount = FloatField('Amount', validators=[InputRequired()])
    apr = FloatField('APR %', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
    submit = SubmitField('Add Debt')

class TransactionFormRange(FlaskForm):
    rangestart = DateField('Range Start', validators=[InputRequired()])
    rangeend = DateField('Range End', validators=[InputRequired()])
    submit1 = SubmitField('Search')

class TransactionDeleteForm(FlaskForm):
    transactionnumber2 = IntegerField('Transaction ID', validators=[InputRequired()])
    submit2 = SubmitField('Submit Deletion')

class TransactionModifyForm(FlaskForm):
    transactionnumber3 = IntegerField('Transaction ID', validators=[InputRequired()])
    transactionamount = FloatField('Total Amount', validators=[InputRequired()])
    transactiondescription = StringField('Description', validators=[InputRequired()])
    transactionmethod = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    transactiondate = DateField('Date', validators=[InputRequired()])
    submit3 = SubmitField('Submit Modifications')

class CustomerModifyForm(FlaskForm):
    accountnumber = IntegerField('Account Number', validators=[InputRequired()])
    customername = StringField('Customer Name', validators=[InputRequired()])
    customerdescription = StringField('Description', validators=[InputRequired()])
    email = StringField('*Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=120)])
    address = StringField('Address', validators=[InputRequired(), Length(max=30)])
    city = StringField('City', validators=[InputRequired(), Length(max=30)])
    state = SelectField('State', choices=[('AL', 'AL'), ('AK', 'AK'), ('AR', 'AR'), ('AZ', 'AZ'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('IA', 'IA'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('MA', 'MA'), ('MD', 'MD'), ('ME', 'ME'), ('MI', 'MI'), ('MN', 'MN'), ('MO', 'MO'), ('MS', 'MS'), ('MT', 'MT'), ('NC', 'NC'), ('NE', 'NE'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NV', 'NV'), ('NY', 'NY'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WI', 'WI'), ('WV', 'WV'), ('WY', 'WY'), ('AS', '*AS'), ('GU', '*GU'), ('MP', '*MP'), ('PR', '*PR'), ('UM', '*UM'), ('VI', '*VI'), ('AA', '*AA'), ('AP', '*AP'), ('AE', '*AE')], validators=[InputRequired()])
    zip = IntegerField('Zip Code', validators=[InputRequired(), NumberRange(max = 99999)])
    term = SelectField('Term',choices=[('DUR', 'Due Upon Receipt'), ('10', 'Net 10'), ('20', 'Net 20'),  ('30', 'Net 30'),  ('45', 'Net 45'), ('60', 'Net 60')], validators=[InputRequired()])
    number = StringField('Phone Number', validators=[InputRequired(), Length(max=30)])
    submit = SubmitField('Submit Modifications')

class VendorModifyForm(FlaskForm):
    accountnumber = IntegerField('Account Number', validators=[InputRequired()])
    vendorname = StringField('Vendor Name', validators=[InputRequired()])
    vendordescription = StringField('Description', validators=[InputRequired()])
    submit = SubmitField('Submit Modifications')

class DebtDeleteForm(FlaskForm):
    accountnumber = IntegerField('Account Number', validators=[InputRequired()])
    submit = SubmitField('Submit Deletion')

class InvestmentDeleteForm(FlaskForm):
    accountnumber = IntegerField('Account Number', validators=[InputRequired()])
    submit = SubmitField('Submit Deletion')

class TransactionDebtForm(FlaskForm):
    accountnumber = SelectField('Which Account', choices=[], validators=[InputRequired()])
    payment = FloatField('Payment Amount', validators=[InputRequired()])
    transactiondate = DateField('Payment Date', validators=[InputRequired()])
    transactionmethod = SelectField('How are you paying', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    submit = SubmitField('Submit Payment')

class PropertyForm(FlaskForm):
    propertyname = StringField('Property Name', validators=[InputRequired(), Length(max=30)])
    propertydescription = StringField('Property Description', validators=[InputRequired(), Length(max=30)])
    propertycost = FloatField('Cost', validators=[InputRequired()])
    propertydate = DateField('Purchase Date', validators=[InputRequired()])
    propertylife = IntegerField('Life Expectancy (in years)', validators=[InputRequired()])

class PropertyDeleteForm(FlaskForm):
    propertyid = IntegerField('Property ID', validators=[InputRequired()])
    submit = SubmitField('Submit Deletion')

class ReceivableForm(FlaskForm):
    transactionsource = SelectField('Customer', choices=[], coerce=int)
    transactiondescription = StringField('Description / P.O. #', validators=[InputRequired()])
    pretaxtotal = FloatField('Pre-Tax Total', validators=[InputRequired()])
    salestax = FloatField('Sales Tax *only if there is sales tax', default=0, validators=[InputRequired()])
    totalamount = FloatField('Total Amount', render_kw={'readonly': True}, validators=[InputRequired()])
    transactionmethod = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    duedate = DateField('Due Date', validators=[InputRequired()])
    transactionreason = SelectField('Reason', choices=[('Sales', 'Sales'), ('Services', 'Services'), ('Other Income', 'Other Income')] , validators=[InputRequired()])

class PayableForm(FlaskForm):
    transactionsource = SelectField('Vendor', choices=[], coerce=int)
    transactiondescription = StringField('Description / P.O. #', validators=[InputRequired()])
    pretaxtotal = FloatField('Pre-Tax Total', validators=[InputRequired()])
    salestax = FloatField('Sales Tax *only if there is sales tax', default=0, validators=[InputRequired()])
    totalamount = FloatField('Total Amount', render_kw={'readonly': True}, validators=[InputRequired()])
    transactionmethod = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    duedate = DateField('Due Date', validators=[InputRequired()])
    transactionreason = SelectField('Reason', choices=[('Payroll', 'Payroll'), ('Utilities', 'Utilities'), ('Advertisements', 'Advertisements'), ('Cost of Materials', 'Cost of Materials'), ('Employee Benefits', 'Employee Benefits'), ('Insurance', 'Insurance'), ('Maintenance', 'Maintenance'), ('Office Supplies', 'Office Supplies'), ('Travel', 'Travel'), ('Shipping', 'Shipping'), ('Returns', 'Returns'), ('Other Expense', 'Other Expense')] , validators=[InputRequired()])

class PayableModifyForm(FlaskForm):
    payableid = IntegerField('Payable ID', validators=[InputRequired()])
    transactionamount = FloatField('Total Amount', validators=[InputRequired()])
    transactiondescription = StringField('Description / P.O. #', validators=[InputRequired()])
    transactionmethod = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    duedate = DateField('Due Date', validators=[InputRequired()])
    submit3 = SubmitField('Submit Modifications')

class ReceivableModifyForm(FlaskForm):
    receivableid = IntegerField('Invoice ID', validators=[InputRequired()])
    transactionamount = FloatField('Total Amount', validators=[InputRequired()])
    transactiondescription = StringField('Description / P.O. #', validators=[InputRequired()])
    transactionmethod = SelectField('Method', choices=[('Cash', 'Cash'), ('EFT', 'EFT'), ('Check', 'Check')] , validators=[InputRequired()])
    duedate = DateField('Due Date', validators=[InputRequired()])
    submit3 = SubmitField('Submit Modifications')

class StatementFormRange(FlaskForm):
    rangestart = DateField('Start Date', validators=[InputRequired()])
    rangeend = DateField('End Date', validators=[InputRequired()])
    submit = SubmitField('Search')

class RecPayPaid(FlaskForm):
    transactionnumber = IntegerField('ID', validators=[InputRequired()])
    transactiondate = DateField('Date Paid', validators=[InputRequired()])
    submit = SubmitField('Mark Paid')

class RecPayDelete(FlaskForm):
    transactionnumber2 = IntegerField('ID', validators=[InputRequired()])
    submit2 = SubmitField('Delete')

class AccountDelete(FlaskForm):
    accountnumber1 = IntegerField('Account Number', validators=[InputRequired()])
    submit1 = SubmitField('Delete')

class AccountModify(FlaskForm):
    accountnumber = IntegerField('Account Number', validators=[InputRequired()])
    accountname = StringField('Name', validators=[InputRequired()])
    accountdescription = StringField('Description', validators=[InputRequired()])
    accountdate = DateField('Date', validators=[InputRequired()])
    submit = SubmitField('Submit Changes')

class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Feedback', validators=[InputRequired(), Length(min=30)])
    submit = SubmitField('Submit')

class BugReportForm(FlaskForm):
    bugtype = SelectField('Type of Bug', choices=[('UI/Graphical', 'UI/Graphical'), ('Data Shown', 'Data Shown'), ('Other', 'Other')] , validators=[InputRequired()])
    report = TextAreaField('Please describe what you experienced', validators=[InputRequired(), Length(min=30)])
    submit = SubmitField('Submit')

class InfoForm(FlaskForm):
    serenade = IntegerField('HiddenSerenade', validators=[InputRequired()])

class ChangePassword(FlaskForm):
    currentpassword = PasswordField('Current Password:', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('validatepassword', message='Your passwords did not match.'), Length(min=8, max=80)])
    validatepassword = PasswordField('Validate New Password', validators=[InputRequired(), Length(min=4, max=40)])
    submit2 = SubmitField('Submit')

class ChangeEmail(FlaskForm):
    currentemail = StringField('Current Email:', validators=[InputRequired()])
    newemail = StringField('New Email:', validators=[InputRequired(), EqualTo('validateemail', message='Your emails did not match.')])
    validateemail = StringField('Validate New Email', validators=[InputRequired()])
    submit3 = SubmitField('Submit')

class ChangeBusinessName(FlaskForm):
    newname = StringField('New Name:', validators=[InputRequired(), EqualTo('validatename', message='Your names did not match.')])
    validatename = StringField('Validate Name:', validators=[InputRequired()])
    submit4 = SubmitField('Submit')

class ChangeBusinessNumber(FlaskForm):
    newnumber = IntegerField('New Number:', validators=[InputRequired(), EqualTo('validatenumber', message='Your numbers did not match.')])
    validatenumber = IntegerField('Validate Number:', validators=[InputRequired()])
    submit5 = SubmitField('Submit')

class ChangeBusinessWebsite(FlaskForm):
    newsite = StringField('New Website URL:', validators=[InputRequired(), EqualTo('validatesite', message='Your website URLs did not match.')])
    validatesite = StringField('Validate URL:', validators=[InputRequired()])
    submit6 = SubmitField('Submit')

class UpdateBalance(FlaskForm):
    newbalance = StringField('New Balance:', validators=[InputRequired(), EqualTo('validatebalance', message='Your balance amounts did not match.')])
    validatebalance = StringField('Validate Balance:', validators=[InputRequired()])
    submit7 = SubmitField('Submit')

class UpdateFiscal(FlaskForm):
    startyear = DateField('Start of Fiscal Year:', validators=[InputRequired()])
    endyear = DateField('End of Fiscal Year:', validators=[InputRequired()])
    submit8 = SubmitField('Submit')

class UpdateLogo(FlaskForm):
    businesslogo = FileField('Business Logo', validators=[FileAllowed(['jpg', 'png']), InputRequired()])
    submit9 = SubmitField('Submit')

class ChangeBusinessAddress(FlaskForm):
    newaddress = StringField('New Address:', validators=[InputRequired()])
    newcity = StringField('New City:', validators=[InputRequired()])
    newzip = IntegerField('New Zipcode:', validators=[InputRequired()])
    newstate = SelectField('New State', choices=[('AL', 'AL'), ('AK', 'AK'), ('AR', 'AR'), ('AZ', 'AZ'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('IA', 'IA'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('MA', 'MA'), ('MD', 'MD'), ('ME', 'ME'), ('MI', 'MI'), ('MN', 'MN'), ('MO', 'MO'), ('MS', 'MS'), ('MT', 'MT'), ('NC', 'NC'), ('NE', 'NE'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NV', 'NV'), ('NY', 'NY'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WI', 'WI'), ('WV', 'WV'), ('WY', 'WY'), ('AS', '*AS'), ('GU', '*GU'), ('MP', '*MP'), ('PR', '*PR'), ('UM', '*UM'), ('VI', '*VI'), ('AA', '*AA'), ('AP', '*AP'), ('AE', '*AE')], validators=[InputRequired()])
    submit10 = SubmitField('Submit')

class MembershipIssueButton(FlaskForm):
    submit = SubmitField('Send Issue Submission')

class ContactForm(FlaskForm):
    name = StringField(label=None, validators=[InputRequired()], render_kw={"placeholder": "Name", "class": "form-control"})
    email = StringField(label=None, validators=[InputRequired()], render_kw={"placeholder": "Email", "class": "form-control"})
    message = TextAreaField(label=None, validators=[InputRequired()], render_kw={"placeholder": "Message", "class": "form-control"})
    submit = SubmitField('Send Message', render_kw={"style": "color: #18d621"})

class RequestResetForm(FlaskForm):
    email = StringField('Email linked to account:', validators=[InputRequired()])
    submit = SubmitField('Request Password Reset')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('validatepassword', message='Your passwords did not match.'), Length(min=8, max=80)])
    validatepassword = PasswordField('Validate Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Reset Password')

class EmailListForm(FlaskForm):
    email2 = StringField("Email", validators=[InputRequired()], render_kw={"placeholder": "Email", "class": "form-control"})
    submit2 = SubmitField('Subscribe', render_kw={"style": "background-color: #18d621 !important;"})

class ContactPageForm(FlaskForm):
    name3 = StringField(label=None, validators=[InputRequired()], render_kw={"placeholder": "Name", "class": "form-control"})
    email3 = StringField(label=None, validators=[InputRequired()], render_kw={"placeholder": "Email", "class": "form-control"})
    message3 = TextAreaField(label=None, validators=[InputRequired()], render_kw={"placeholder": "Message", "class": "form-control"})
    submit3 = SubmitField('Send Message', render_kw={"style": "background-color: #18d621 !important;"})