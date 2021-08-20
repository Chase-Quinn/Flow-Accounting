from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar

def sort7day(query):
    result = [0, 0, 0, 0, 0, 0, 0]
    for queries in query:
        if queries.transactiondate == (date.today()-timedelta(days=6)):
            result[0] = queries.totalamount + result[0]
        elif queries.transactiondate == (date.today()-timedelta(days=5)):
            result[1] = queries.totalamount + result[1]
        elif queries.transactiondate == (date.today()-timedelta(days=4)):
            result[2] = queries.totalamount + result[2]
        elif queries.transactiondate == (date.today()-timedelta(days=3)):
            result[3] = queries.totalamount + result[3]
        elif queries.transactiondate == (date.today()-timedelta(days=2)):
            result[4] = queries.totalamount + result[4]
        elif queries.transactiondate == (date.today()-timedelta(days=1)):
            result[5] = queries.totalamount + result[5]
        elif queries.transactiondate == date.today():
            result[6] = queries.totalamount + result[6]
        
    return result

def sortmonth(query):
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for queries in query:
        if queries.transactiondate == (date.today()-timedelta(days=29)):
            result[0] = queries.totalamount + result[0]
        elif queries.transactiondate == (date.today()-timedelta(days=28)):
            result[1] = queries.totalamount + result[1]
        elif queries.transactiondate == (date.today()-timedelta(days=27)):
            result[2] = queries.totalamount + result[2]
        elif queries.transactiondate == (date.today()-timedelta(days=26)):
            result[3] = queries.totalamount + result[3]
        elif queries.transactiondate == (date.today()-timedelta(days=25)):
            result[4] = queries.totalamount + result[4]
        elif queries.transactiondate == (date.today()-timedelta(days=24)):
            result[5] = queries.totalamount + result[5]
        elif queries.transactiondate == (date.today()-timedelta(days=23)):
            result[6] = queries.totalamount + result[6]
        elif queries.transactiondate == (date.today()-timedelta(days=22)):
            result[7] = queries.totalamount + result[7]
        elif queries.transactiondate == (date.today()-timedelta(days=21)):
            result[8] = queries.totalamount + result[8]
        elif queries.transactiondate == (date.today()-timedelta(days=20)):
            result[9] = queries.totalamount + result[9]
        elif queries.transactiondate == (date.today()-timedelta(days=19)):
            result[10] = queries.totalamount + result[10]
        elif queries.transactiondate == (date.today()-timedelta(days=18)):
            result[11] = queries.totalamount + result[11]
        elif queries.transactiondate == (date.today()-timedelta(days=17)):
            result[12] = queries.totalamount + result[12]
        elif queries.transactiondate == (date.today()-timedelta(days=16)):
            result[13] = queries.totalamount + result[13]
        elif queries.transactiondate == (date.today()-timedelta(days=15)):
            result[14] = queries.totalamount + result[14]
        elif queries.transactiondate == (date.today()-timedelta(days=14)):
            result[15] = queries.totalamount + result[15]
        elif queries.transactiondate == (date.today()-timedelta(days=13)):
            result[16] = queries.totalamount + result[16]
        elif queries.transactiondate == (date.today()-timedelta(days=12)):
            result[17] = queries.totalamount + result[17]
        elif queries.transactiondate == (date.today()-timedelta(days=11)):
            result[18] = queries.totalamount + result[18]
        elif queries.transactiondate == (date.today()-timedelta(days=10)):
            result[19] = queries.totalamount + result[19]
        elif queries.transactiondate == (date.today()-timedelta(days=9)):
            result[20] = queries.totalamount + result[20]
        elif queries.transactiondate == (date.today()-timedelta(days=8)):
            result[21] = queries.totalamount + result[21]
        elif queries.transactiondate == (date.today()-timedelta(days=7)):
            result[22] = queries.totalamount + result[22]
        elif queries.transactiondate == (date.today()-timedelta(days=6)):
            result[23] = queries.totalamount + result[23]
        elif queries.transactiondate == (date.today()-timedelta(days=5)):
            result[24] = queries.totalamount + result[24]
        elif queries.transactiondate == (date.today()-timedelta(days=4)):
            result[25] = queries.totalamount + result[25]
        elif queries.transactiondate == (date.today()-timedelta(days=3)):
            result[26] = queries.totalamount + result[26]
        elif queries.transactiondate == (date.today()-timedelta(days=2)):
            result[27] = queries.totalamount + result[27]
        elif queries.transactiondate == (date.today()-timedelta(days=1)):
            result[28] = queries.totalamount + result[28]
        elif queries.transactiondate == date.today():
            result[29] = queries.totalamount + result[29]

    return result

def sortthreemonth(query):
    result = [0, 0, 0]
    currentdate = date.today()
    secondmonth = currentdate - relativedelta(months = 1)
    thirdmonth = currentdate - relativedelta(months = 2)
    fourthmonth = currentdate - relativedelta(months = 3)
    for queries in query:
        if fourthmonth <= queries.transactiondate and queries.transactiondate.month == thirdmonth.month:
            result[0] = queries.totalamount + result[0]
        elif thirdmonth <= queries.transactiondate and queries.transactiondate.month == secondmonth.month:
            result[1] = queries.totalamount + result[1]
        elif secondmonth <= queries.transactiondate and queries.transactiondate.month == currentdate.month:
            result[2] = queries.totalamount + result[2]

    return result

def sortsixmonth(query):
    result = [0, 0, 0, 0, 0, 0]
    currentdate = date.today()
    secondmonth = currentdate - relativedelta(months = 1)
    thirdmonth = currentdate - relativedelta(months = 2)
    fourthmonth = currentdate - relativedelta(months = 3)
    fifthmonth = currentdate - relativedelta(months = 4)
    sixthmonth = currentdate - relativedelta(months = 5)
    seventhmonth = currentdate - relativedelta(months = 6)
    for queries in query:
        if seventhmonth <= queries.transactiondate and queries.transactiondate.month == sixthmonth.month:
            result[0] = queries.totalamount + result[0]
        elif sixthmonth <= queries.transactiondate and queries.transactiondate.month == fifthmonth.month:
            result[1] = queries.totalamount + result[1]
        elif fifthmonth <= queries.transactiondate and queries.transactiondate.month == fourthmonth.month:
            result[2] = queries.totalamount + result[2]
        elif fourthmonth <= queries.transactiondate and queries.transactiondate.month == thirdmonth.month:
            result[3] = queries.totalamount + result[3]
        elif thirdmonth <= queries.transactiondate and queries.transactiondate.month == secondmonth.month:
            result[4] = queries.totalamount + result[4]
        elif secondmonth <= queries.transactiondate and queries.transactiondate.month == currentdate.month:
            result[5] = queries.totalamount + result[5]

    return result

def sortyear(query):
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    currentdate = date.today()
    secondmonth = currentdate - relativedelta(months = 1)
    thirdmonth = currentdate - relativedelta(months = 2)
    fourthmonth = currentdate - relativedelta(months = 3)
    fifthmonth = currentdate - relativedelta(months = 4)
    sixthmonth = currentdate - relativedelta(months = 5)
    seventhmonth = currentdate - relativedelta(months = 6)
    eighthmonth = currentdate - relativedelta(months = 7)
    ninthmonth = currentdate - relativedelta(months = 8)
    tenthmonth = currentdate - relativedelta(months = 9)
    eleventhmonth = currentdate - relativedelta(months = 10)
    twelfthmonth = currentdate - relativedelta(months = 11)
    thirteenthmonth = currentdate - relativedelta(months = 12)
    for queries in query:
        if thirteenthmonth <= queries.transactiondate and queries.transactiondate.month == twelfthmonth.month:
            result[0] = queries.totalamount + result[0]
        elif twelfthmonth <= queries.transactiondate and queries.transactiondate.month == eleventhmonth.month:
            result[1] = queries.totalamount + result[1]
        elif eleventhmonth <= queries.transactiondate and queries.transactiondate.month == tenthmonth.month:
            result[2] = queries.totalamount + result[2]
        elif tenthmonth <= queries.transactiondate and queries.transactiondate.month == ninthmonth.month:
            result[3] = queries.totalamount + result[3]
        elif ninthmonth <= queries.transactiondate and queries.transactiondate.month == eighthmonth.month:
            result[4] = queries.totalamount + result[4]
        elif eighthmonth <= queries.transactiondate and queries.transactiondate.month == seventhmonth.month:
            result[5] = queries.totalamount + result[5]
        elif seventhmonth <= queries.transactiondate and queries.transactiondate.month == sixthmonth.month:
            result[6] = queries.totalamount + result[6]
        elif sixthmonth <= queries.transactiondate and queries.transactiondate.month == fifthmonth.month:
            result[7] = queries.totalamount + result[7]
        elif fifthmonth <= queries.transactiondate and queries.transactiondate.month == fourthmonth.month:
            result[8] = queries.totalamount + result[8]
        elif fourthmonth <= queries.transactiondate and queries.transactiondate.month == thirdmonth.month:
            result[9] = queries.totalamount + result[9]
        elif thirdmonth <= queries.transactiondate and queries.transactiondate.month == secondmonth.month:
            result[10] = queries.totalamount + result[10]
        elif secondmonth <= queries.transactiondate and queries.transactiondate.month == currentdate.month:
            result[11] = queries.totalamount + result[11]
    
    return result

def sortthreeyear(query):
    result = [0, 0, 0]
    currentdate = date.today()
    secondyear = currentdate - relativedelta(years = 1)
    thirdyear = currentdate - relativedelta(years = 2)
    fourthyear = currentdate - relativedelta(years = 3)
    for queries in query:
        if fourthyear <= queries.transactiondate and queries.transactiondate.year == thirdyear.year:
            result[0] = queries.totalamount + result[0]
        elif thirdyear <= queries.transactiondate and queries.transactiondate.year == secondyear.year:
            result[1] = queries.totalamount + result[1]
        elif secondyear <= queries.transactiondate and queries.transactiondate.year == currentdate.year:
            result[2] = queries.totalamount + result[2]

    return result

def sortfiveyear(query):
    result = [0, 0, 0, 0, 0]
    currentdate = date.today()
    secondyear = currentdate - relativedelta(years = 1)
    thirdyear = currentdate - relativedelta(years = 2)
    fourthyear = currentdate - relativedelta(years = 3)
    fifthyear = currentdate - relativedelta(years = 4)
    sixthyear = currentdate - relativedelta(years = 5)
    for queries in query:
        if sixthyear <= queries.transactiondate and queries.transactiondate.year == fifthyear.year:
            result[0] = queries.totalamount + result[0]
        elif fifthyear <= queries.transactiondate and queries.transactiondate.year == secondyear.year:
            result[1] = queries.totalamount + result[1]
        elif fourthyear <= queries.transactiondate and queries.transactiondate.year == thirdyear.year:
            result[2] = queries.totalamount + result[2]
        elif thirdyear <= queries.transactiondate and queries.transactiondate.year == secondyear.year:
            result[3] = queries.totalamount + result[3]
        elif secondyear <= queries.transactiondate and queries.transactiondate.year == currentdate.year:
            result[4] = queries.totalamount + result[4]

    return result

def addTotals(query):
    total = 0
    for queries in query:
        total = queries.totalamount + total

    return total

def addOther(query):
    total = 0
    for queries in query:
        if queries.transactionreason != 'Utilities':
            if queries.transactionreason != 'Payroll':
                if queries.transactionreason != 'Advertisements':
                    total = queries.totalamount + total

    return total