    /////////////////////////////////////////////////////////////////////////////////////
//        The Class below handles all data needed              //////////////////////
//          from the server for the Charts                     //////////////////////
//                 to function properly                        //////////////////////
//                  check the comments                         //////////////////////
/////////////////////////////////////////////////////////////////////////////////////
var a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u;
//////////////////////////////////////////////////////////////////////
////////////////////////////////////                        CHART DATA
//////////////////////////////////////////////////////////////////////
b = {{ sevendayincomedata }};
var x = 0;
var len = b.length
while(x < len){ 
    b[x] = b[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the Revenue week line chart, this is 7 values from the last 7 days
c = {{ monthincomedata }};
var x = 0;
var len = c.length
while(x < len){ 
    c[x] = c[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the Revenue month line chart, this is 30 values from the last 30 days
d = {{ threemonthincomedata }};
var x = 0;
var len = d.length
while(x < len){ 
    d[x] = d[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the Revenue 3-month line chart, this is 3 values from the last three months
e = {{ sixmonthincomedata }};
var x = 0;
var len = e.length
while(x < len){ 
    e[x] = e[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the Revenue 6-month line chart, this is 6 values from the last six months
f = {{ yearincomedata }};
var x = 0;
var len = f.length
while(x < len){ 
    f[x] = f[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the Revenue year line chart, this is 12 values from the last year
g = {{ threeyearincomedata }};
var x = 0;
var len = g.length
while(x < len){ 
    g[x] = g[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the Revenue 3-year line chart, this is 3 values from the last 3 years
h = {{ fiveyearincomedata }};
var x = 0;
var len = h.length
while(x < len){ 
    h[x] = h[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the 5-year line chart, this is 5 values from the last 5 years

//////////////////////////////////////////////////////////////////////
////////////////////////////////////                      EXPENSE DATA
//////////////////////////////////////////////////////////////////////
j = {{ sevendayexpensedata }};
var x = 0;
var len = j.length
while(x < len){ 
    j[x] = j[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the EXPENSE week line chart, this is 7 values from the last 7 days
k = {{ monthexpensedata }};
var x = 0;
var len = k.length
while(x < len){ 
    k[x] = k[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the EXPENSE month line chart, this is 30 values from the last 30 days
l = {{ threemonthexpensedata }};
var x = 0;
var len = l.length
while(x < len){ 
    l[x] = l[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the EXPENSE 3-month line chart, this is 3 values from the last three months
m = {{ sixmonthexpensedata }};
var x = 0;
var len = m.length
while(x < len){ 
    m[x] = m[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the EXPENSE 6-month line chart, this is 6 values from the last six months
n = {{ yearexpensedata }};
var x = 0;
var len = n.length
while(x < len){ 
    n[x] = n[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the EXPENSE year line chart, this is 12 values from the last year
o = {{ threeyearexpensedata }};
var x = 0;
var len = o.length
while(x < len){ 
    o[x] = o[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the EXPENSE 3-year line chart, this is 3 values from the last 3 years
p = {{ fiveyearexpensedata }};
var x = 0;
var len = p.length
while(x < len){ 
    p[x] = p[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the EXPENSE line chart, this is 5 values from the last 5 years

//////////////////////////////////////////////////////////////////////
////////////////////////////////////                      PIE/BAR DATA
//////////////////////////////////////////////////////////////////////
q = {{ totalexpenses }};

//this variable contains placeholder data for Fiscal YTD TOTAL EXPENSES within the pie/bar charts
r = {{ totalincome }};
//this variable contains placeholder data for Fiscal YTD TOTAL INCOME within the pie/bar charts
// s = 2348.16.toFixed(2);
//this variable contains placeholder data for Fiscal YTD TOTAL MONTHLY OPERATING EXPENSES, it should be for a single month **e.g. 4432.33/month, only need the numeric value
t = [{{ sales }}, {{ services }}, {{ otherincome }}];
var x = 0;
var len = t.length
while(x < len){ 
    t[x] = t[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the income part of the pie/bar graph, this is where the total income gets broken down, array is [sales, donations, taxes]
u = [{{ utilities }}, {{ payroll }}, {{ advertisements }}, {{ otherexpense }}];
var x = 0;
var len = u.length
while(x < len){ 
    u[x] = u[x].toFixed(2); 
    x++
}
//this variable contains placeholder data for the expenses part of the pie/bar graph, this is where the total expenses gets broken down, array is
//[Operating Expenses, Payroll, Material Costs, Advertising Costs, Charitable Donations]

class ServerLoad {
    constructor(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
        this.e = e;
        this.f = f;
        this.g = g;
        this.h = h;
        this.i = i;
        this.j = j;
        this.k = k;
        this.l = l;
        this.m = m;
        this.n = n;
        this.o = o;
        this.p = p;
        this.q = q;
        this.r = r;
        this.s = s;
        this.t = t;
        this.u = u;

    }
}

var a = new ServerLoad(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u);



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////// EVERTHING BELOW IS FOR GRAPH APPLICATIONS ///////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function sizeLineGraph() {
    var width, height, canvas, cont, contSize, currentLabels, currentHeading;
    cont = document.getElementById('lineChartSection');
    contSize = getComputedStyle(cont);
    width = parseInt(contSize.getPropertyValue('width'), 10);
    height = parseInt(contSize.getPropertyValue('height'), 10);
    canvas = document.getElementById('flowLine');
    canvas.width = width;
    canvas.height = height;
}

function sizePieGraph() {
    var width, height, canvas, cont, contSize, currentLabels, currentHeading;
    cont = document.getElementById('pieChartSection');
    contSize = getComputedStyle(cont);
    width = parseInt(contSize.getPropertyValue('width'), 10);
    height = parseInt(contSize.getPropertyValue('height'), 10);
    canvas = document.getElementById('flowPie');
    canvas.width = width;
    canvas.height = height;
}

/////////////////////////////////////////////////////////////////////////////////////
//         EVERYTHING ABOVE IS FOR FORMATTING                  //////////////////////
/////////////////////////////////////////////////////////////////////////////////////

class Graph {
    constructor(type, labels, heading, data, backgroundColor, borderColor) {
        this.type = type;
        this.labels = labels;
        this.heading = heading;
        this.data = data;
        this.backgroundColor = backgroundColor;
        this.borderColor = borderColor;
    }
}

/////////////////////////////////////////////////////////////////////////////////////
//         LINE GRAPHS                                         //////////////////////
/////////////////////////////////////////////////////////////////////////////////////
// Date Functions/Objects for getting proper labels
var date = new Date();

function getDay() {
    var currentDay = date.getDay();
    return currentDay;
}

currentDay = getDay();

function getMonth() {
    var currentMonth = date.getMonth();
    return currentMonth;
}

currentMonth = getMonth();

function getYear() {
    var currentYear = date.getYear();
    return currentYear;
}

currentYear = getYear();

function getDayLabels() {
    var currentDate = new Date();
    hour = currentDate.getHours();
    var a;
    var dayLabels = [];
    for (i = 0; i < 25; i++) {
        if (hour == 0) {
            hour = 24;
            a = '12am'
            dayLabels.unshift(a);
        }
        else if (hour > 12 && hour < 24) {
            var b = hour - 12;
            a = b + 'pm';
            dayLabels.unshift(a);
        }
        else if (hour < 12 && hour > 0) {
            a = hour + 'am';
            dayLabels.unshift(a);
        }
        hour--;
    }

    return dayLabels;
}

function getWeekLabels(currentDay) {
    switch (currentDay) {
        case 0:
            //if the day is sunday
            weekLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
            return weekLabels;
            break;
        case 1:
            //if the day is monday
            weekLabels = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday'];
            return weekLabels;
            break;
        case 2:
            //if the day is tuesday
            weekLabels = ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday'];
            return weekLabels;
            break;
        case 3:
            //if the day is wednesday
            weekLabels = ['Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday'];
            return weekLabels;
            break;
        case 4:
            //if the day is thursday
            weekLabels = ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'];
            return weekLabels;
            break;
        case 5:
            //if the day is friday
            weekLabels = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
            return weekLabels;
            break;
        case 6:
            //if the day is saturday
            weekLabels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            return weekLabels;
            break;
        default:
            weekLabels = 'Error with the server, please try again later.';
    }
}

//this is to check for leap years for proper dates on month labels
function leapCheck() {
    var leapYear;
    var year = Date.getUTCFullYear;
    var b = Number(year);
    if ((a % 4) == 0) {
        leapYear = true;
    }
    else {
        leapYear = false;
    }

    return leapYear;
}

function getMonthlabels() {
    var monthLabels = [];
    var currentDate = new Date();
    var month = currentDate.getUTCMonth() + 1;
    var day = currentDate.getUTCDate();
    var year = currentDate.getUTCFullYear();
    var leapYear = leapCheck();

    for (var i = 0; i < 30; i++) {
        var j = month + '/' + day;
        monthLabels.unshift(j);
        day--;
        if (day == 0) {
            if (month != 1) {
                month--;
                if (day == 0) {
                    if (month == 0 || month == 2 || month == 4 || month == 6 || month == 7 || month == 8 || month == 10 || month == 12) {
                        day = 32;
                    }
                    if (month == 3 || month == 5 || month == 9 || month == 11) {
                        day = 31;
                    }
                    if (month == 1 && leapYear == false) {
                        day = 29;
                    }
                    if (month == 1 && leapYear == true) {
                        day = 30;
                    }
                }
            }
            else if (month == 1) {
                month = 12;
                if (day == 0) {
                    if (month == 0 || month == 2 || month == 4 || month == 6 || month == 7 || month == 8 || month == 10 || month == 12) {
                        day = 31;
                    }
                    if (month == 3 || month == 5 || month == 9 || month == 11) {
                        day = 30;
                    }
                    if (month == 1 && leapYear == false) {
                        day = 28;
                    }
                    if (month == 1 && leapYear == true) {
                        day = 29;
                    }
                }
            }
        }
    }
    return monthLabels;

    console.log(monthLabels);
}

function getThreeMonthLabels(currentMonth) {
    var jan, feb, mar, apr, may, jun, jul, aug, sept, oct, nov, dec;
    jan = 'Jan';
    feb = 'Feb';
    mar = 'Mar';
    apr = 'Apr';
    may = 'May';
    jun = 'Jun';
    jul = 'Jul';
    aug = 'Aug';
    sept = 'Sept';
    oct = 'Oct';
    nov = 'Nov';
    dec = 'Dec';
    yearLabels = [jan, feb, mar, apr, may, jun, jul, aug, sept, oct, nov, dec];
    switch (currentMonth) {
        case 0:
            //if the month is january
            yearLabels.shift();
            yearLabels.push(jan);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 1:
            //if the month is february
            for (var i = 0; i < 2; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 2:
            //if the month is march
            for (var i = 0; i < 3; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 3:
            //if the month is april
            for (var i = 0; i < 4; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 4:
            //if the month is may
            for (var i = 0; i < 5; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 5:
            //if the month is june
            for (var i = 0; i < 6; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may, jun);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 6:
            //if the month is july
            for (var i = 0; i < 7; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may, jun, jul);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 7:
            //if the month is august
            for (var i = 4; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(sept, oct, nov, dec);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 8:
            //if the month is september
            for (var i = 3; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(oct, nov, dec);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 9:
            //if the month is october
            for (var i = 2; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(nov, dec);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 10:
            //if the month is november
            yearLabels.pop();
            yearLabels.unshift(dec);
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        case 11:
            //if the month is december
            threeMonthLabels = [yearLabels[9], yearLabels[10], yearLabels[11]];
            return threeMonthLabels;
            break;
        default:
            threeMonthLabels = 'Error with the server, please try again later.';
            break;
    }
}

function getSixMonthLabels(currentMonth) {
    var jan, feb, mar, apr, may, jun, jul, aug, sept, oct, nov, dec;
    jan = 'Jan';
    feb = 'Feb';
    mar = 'Mar';
    apr = 'Apr';
    may = 'May';
    jun = 'Jun';
    jul = 'Jul';
    aug = 'Aug';
    sept = 'Sept';
    oct = 'Oct';
    nov = 'Nov';
    dec = 'Dec';
    yearLabels = [jan, feb, mar, apr, may, jun, jul, aug, sept, oct, nov, dec];
    switch (currentMonth) {
        case 0:
            //if the month is january
            yearLabels.shift();
            yearLabels.push(jan);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 1:
            //if the month is february
            for (var i = 0; i < 2; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 2:
            //if the month is march
            for (var i = 0; i < 3; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 3:
            //if the month is april
            for (var i = 0; i < 4; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 4:
            //if the month is may
            for (var i = 0; i < 5; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 5:
            //if the month is june
            for (var i = 0; i < 6; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may, jun);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 6:
            //if the month is july
            for (var i = 0; i < 7; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may, jun, jul);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 7:
            //if the month is august
            for (var i = 4; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(sept, oct, nov, dec);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 8:
            //if the month is september
            for (var i = 3; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(oct, nov, dec);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 9:
            //if the month is october
            for (var i = 2; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(nov, dec);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 10:
            //if the month is november
            yearLabels.pop();
            yearLabels.unshift(dec);
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        case 11:
            //if the month is december
            sixMonthLabels = [yearLabels[6], yearLabels[7], yearLabels[8], yearLabels[9], yearLabels[10], yearLabels[11]];
            return sixMonthLabels;
            break;
        default:
            sixMonthLabels = 'Error with the server, please try again later.';
            break;
    }
}

function getYearLabels(currentMonth) {
    var jan, feb, mar, apr, may, jun, jul, aug, sept, oct, nov, dec;
    jan = 'Jan';
    feb = 'Feb';
    mar = 'Mar';
    apr = 'Apr';
    may = 'May';
    jun = 'Jun';
    jul = 'Jul';
    aug = 'Aug';
    sept = 'Sept';
    oct = 'Oct';
    nov = 'Nov';
    dec = 'Dec';
    yearLabels = [jan, feb, mar, apr, may, jun, jul, aug, sept, oct, nov, dec];
    switch (currentMonth) {
        case 0:
            //if the month is january
            yearLabels.shift();
            yearLabels.push(jan);
            return yearLabels;
            break;
        case 1:
            //if the month is february
            for (var i = 0; i < 2; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb);
            return yearLabels;
            break;
        case 2:
            //if the month is march
            for (var i = 0; i < 3; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar);
            return yearLabels;
            break;
        case 3:
            //if the month is april
            for (var i = 0; i < 4; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr);
            return yearLabels;
            break;
        case 4:
            //if the month is may
            for (var i = 0; i < 5; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may);
            return yearLabels;
            break;
        case 5:
            //if the month is june
            for (var i = 0; i < 6; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may, jun);
            return yearLabels;
            break;
        case 6:
            //if the month is july
            for (var i = 0; i < 7; i++) {
                yearLabels.shift();
            }
            yearLabels.push(jan, feb, mar, apr, may, jun, jul);
            return yearLabels;
            break;
        case 7:
            //if the month is august
            for (var i = 4; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(sept, oct, nov, dec);
            return yearLabels;
            break;
        case 8:
            //if the month is september
            for (var i = 3; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(oct, nov, dec);
            return yearLabels;
            break;
        case 9:
            //if the month is october
            for (var i = 2; i > 0; i--) {
                yearLabels.pop();
            }
            yearLabels.unshift(nov, dec);
            return yearLabels;
            break;
        case 10:
            //if the month is november
            yearLabels.pop();
            yearLabels.unshift(dec);
            return yearLabels;
            break;
        case 11:
            //if the month is december
            return yearLabels;
            break;
        default:
            yearLabels = 'Error with the server, please try again later.';
            break;
    }
}

function getThreeYearLabels(currentYear) {
    var threeYearLabels = [];
    var i = 0;
    var j = 1900;
    var stop = 2;
    for (i; i <= stop; i++) {
        threeYearLabels.unshift(currentYear + j);
        j--;
    }
    return threeYearLabels;
}

function getFiveYearLabels(currentYear) {
    var fiveYearLabels = [];
    var i = 0;
    var j = 1900;
    var stop = 4;
    for (i; i <= stop; i++) {
        fiveYearLabels.unshift(currentYear + j);
        j--;
    }
    return fiveYearLabels;
}
/////////////////////////////////////////////////////////////////////////////////////
//         LINE GRAPH OBJECTS                                  //////////////////////
/////////////////////////////////////////////////////////////////////////////////////
// REVENUE Day Line Chart
// var dayLabels, dayHeading, dayData, dayBackgroundColor, dayBorderColor, dayGraph;
// dayLabels = getDayLabels();
// dayHeading = '24 Hours - Revenue';
// dayData = a.a;
// dayBackgroundColor = 'rgba(21, 243, 21, 0.4)';
// dayBorderColor = 'rgba(2, 58, 2, 0.6)';

// dayGraph = new Graph('line', dayLabels, dayHeading, dayData, dayBackgroundColor, dayBorderColor);

// REVENUE Week Line Chart
var weekLabels, weekHeading, weekData, weekBackgroundColor, weekBorderColor, weekGraph;
weekLabels = getWeekLabels(currentDay);
weekHeading = 'Past Week - Revenue';
weekData = a.b;
weekBackgroundColor = 'rgba(21, 243, 21, 0.4)';
weekBorderColor = 'rgba(2, 58, 2, 0.6)';

weekGraph = new Graph('line', weekLabels, weekHeading, weekData, weekBackgroundColor, weekBorderColor);

// REVENUE Month Line Chart
var monthlabels, monthHeading, monthData, monthBackgroundColor, monthBorderColor, monthGraph;
monthlabels = getMonthlabels();
monthHeading = 'Past Month - Revenue';
monthData = a.c;
monthBackgroundColor = 'rgba(21, 243, 21, 0.4)';
monthBorderColor = 'rgba(2, 58, 2, 0.6)';

monthGraph = new Graph('line', monthlabels, monthHeading, monthData, monthBackgroundColor, monthBorderColor);

// REVENUE Three Month line Chart
var threeMonthLabels, threeMonthHeading, threeMonthData, threeMonthBackgroundColor, threeMonthBorderColor, threeMonthGraph;
threeMonthLabels = getThreeMonthLabels(currentMonth);
threeMonthHeading = 'Past Three Months - Revenue';
threeMonthData = a.d;
threeMonthBackgroundColor = 'rgba(21, 243, 21, 0.4)';
threeMonthBorderColor = 'rgba(2, 58, 2, 0.6)';

threeMonthGraph = new Graph('line', threeMonthLabels, threeMonthHeading, threeMonthData, threeMonthBackgroundColor, threeMonthBorderColor);

// REVENUE Six Month line Chart
var sixMonthLabels, sixMonthHeading, sixMonthData, sixMonthBackgroundColor, sixMonthBorderColor, sixMonthGraph;
sixMonthLabels = getSixMonthLabels(currentMonth);
sixMonthHeading = 'Past Six Months - Revenue';
sixMonthData = a.e;
sixMonthBackgroundColor = 'rgba(21, 243, 21, 0.4)';
sixMonthBorderColor = 'rgba(2, 58, 2, 0.6)';

sixMonthGraph = new Graph('line', sixMonthLabels, sixMonthHeading, sixMonthData, sixMonthBackgroundColor, sixMonthBorderColor);

// REVENUE One Year Line Chart
var YearLabels, YearHeading, yearData, yearBackgroundColor, yearBorderColor;
yearLabels = getYearLabels(currentMonth);
yearHeading = 'Past Year - Revenue';
yearData = a.f;
yearBackgroundColor = 'rgba(21, 243, 21, 0.4)';
yearBorderColor = 'rgba(2, 58, 2, 0.6)';

yearGraph = new Graph('line', yearLabels, yearHeading, yearData, yearBackgroundColor, yearBorderColor);

// REVENUE Three Year Line Chart
var threeYearLabels, threeYearHeading, threeYearData, threeYearBackgroundColor, threeYearBorderColor;
threeYearLabels = getThreeYearLabels(currentYear);
threeYearHeading = 'Past Three Years - Revenue';
threeYearData = a.g;
threeYearBackgroundColor = 'rgba(21, 243, 21, 0.4)';
threeYearBorderColor = 'rgba(2, 58, 2, 0.6)';

threeYearGraph = new Graph('line', threeYearLabels, threeYearHeading, threeYearData, threeYearBackgroundColor, threeYearBorderColor);

// REVENUE Five Year Line Chart
var fiveYearLabels, fiveYearHeading, fiveYearData, fiveYearBackgroundColor, fiveYearBorderColor;
fiveYearLabels = getFiveYearLabels(currentYear);
fiveYearHeading = 'Past Five Years - Revenue';
fiveYearData = a.h;
fiveYearBackgroundColor = 'rgba(21, 243, 21, 0.4)';
fiveYearBorderColor = 'rgba(2, 58, 2, 0.6)';

fiveYearGraph = new Graph('line', fiveYearLabels, fiveYearHeading, fiveYearData, fiveYearBackgroundColor, fiveYearBorderColor);

// EXPENSE Day Line Chart
// var dayLabels, dayExpenseHeading, dayExpenseData, dayExpenseBackgroundColor, dayExpenseBorderColor, dayExpenseGraph;
// dayLabels = getDayLabels();
// dayExpenseHeading = '24 Hours - Expenses';
// dayExpenseData = a.i;
// dayExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
// dayExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

// dayExpenseGraph = new Graph('line', dayLabels, dayExpenseHeading, dayExpenseData, dayExpenseBackgroundColor, dayExpenseBorderColor);

// EXPENSE Week Line Chart
var weekLabels, weekExpenseHeading, weekExpenseData, weekExpenseBackgroundColor, weekExpenseBorderColor, weekExpenseGraph;
weekLabels = getWeekLabels(currentDay);
weekExpenseHeading = 'Past Week - Expenses';
weekExpenseData = a.j;
weekExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
weekExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

weekExpenseGraph = new Graph('line', weekLabels, weekExpenseHeading, weekExpenseData, weekExpenseBackgroundColor, weekExpenseBorderColor);

// EXPENSE Month Line Chart
var monthlabels, monthExpenseHeading, monthExpenseData, monthExpenseBackgroundColor, monthExpenseBorderColor, monthExpenseGraph;
monthlabels = getMonthlabels();
monthExpenseHeading = 'Past Month - Expenses';
monthExpenseData = a.k;
monthExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
monthExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

monthExpenseGraph = new Graph('line', monthlabels, monthExpenseHeading, monthExpenseData, monthExpenseBackgroundColor, monthExpenseBorderColor);

// EXPENSE Three Month line Chart
var threeMonthLabels, threeMonthExpenseHeading, threeMonthExpenseData, threeMonthExpenseBackgroundColor, threeMonthExpenseBorderColor, threeMonthExpenseGraph;
threeMonthLabels = getThreeMonthLabels(currentMonth);
threeMonthExpenseHeading = 'Past Three Months - Expenses';
threeMonthExpenseData = a.l;
threeMonthExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
threeMonthExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

threeMonthExpenseGraph = new Graph('line', threeMonthLabels, threeMonthExpenseHeading, threeMonthExpenseData, threeMonthExpenseBackgroundColor, threeMonthExpenseBorderColor);

// EXPENSE Six Month line Chart
var sixMonthLabels, sixMonthExpenseHeading, sixMonthExpenseData, sixMonthExpenseBackgroundColor, sixMonthExpenseBorderColor, sixMonthExpenseGraph;
sixMonthLabels = getSixMonthLabels(currentMonth);
sixMonthExpenseHeading = 'Past Six Months - Expenses';
sixMonthExpenseData = a.m;
sixMonthExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
sixMonthExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

sixMonthExpenseGraph = new Graph('line', sixMonthLabels, sixMonthExpenseHeading, sixMonthExpenseData, sixMonthExpenseBackgroundColor, sixMonthExpenseBorderColor);

// EXPENSE One Year Line Chart
var YearLabels, YearExpenseHeading, yearExpenseData, yearExpenseBackgroundColor, yearExpenseBorderColor;
yearLabels = getYearLabels(currentMonth);
yearExpenseHeading = 'Past Year - Expenses';
yearExpenseData = a.n;
yearExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
yearExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

yearExpenseGraph = new Graph('line', yearLabels, yearExpenseHeading, yearExpenseData, yearExpenseBackgroundColor, yearExpenseBorderColor);

// EXPENSE Three Year Line Chart
var threeYearLabels, threeYearExpenseHeading, threeYearExpenseData, threeYearExpenseBackgroundColor, threeYearExpenseBorderColor;
threeYearLabels = getThreeYearLabels(currentYear);
threeYearExpenseHeading = 'Past Three Years - Expenses';
threeYearExpenseData = a.o;
threeYearExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
threeYearExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

threeYearExpenseGraph = new Graph('line', threeYearLabels, threeYearExpenseHeading, threeYearExpenseData, threeYearExpenseBackgroundColor, threeYearExpenseBorderColor);

// EXPENSES Five Year Line Chart
var fiveYearLabels, fiveYearExpenseHeading, fiveYearExpenseData, fiveYearExpenseBackgroundColor, fiveYearExpenseBorderColor;
fiveYearLabels = getFiveYearLabels(currentYear);
fiveYearExpenseHeading = 'Past Five Years - Expenses';
fiveYearExpenseData = a.p;
fiveYearExpenseBackgroundColor = 'rgba(255, 19, 3, 0.4)';
fiveYearExpenseBorderColor = 'rgba(128, 10, 1, 0.6)';

fiveYearExpenseGraph = new Graph('line', fiveYearLabels, fiveYearExpenseHeading, fiveYearExpenseData, fiveYearExpenseBackgroundColor, fiveYearExpenseBorderColor);

/////////////////////////////////////////////////////////////////////////////////////
//          BELOW GENERATES THE LINE GRAPHS                    //////////////////////
/////////////////////////////////////////////////////////////////////////////////////

function resetCanvas() { //FIXES ONHOVER GLITCH WHERE IT JUMPS BETWEEN PRIOR GRAPHS
    $('#flowLine').remove();
    $('#lineChartSection').append('<canvas id="flowLine"><canvas>');
    canvas = document.querySelector('#flowLine');
    ctx = canvas.getContext('2d');
    sizeLineGraph();
};

//REVENUE LINE CHARTS START////////////////////////////////////////////////////

// function generateDayGraph() {
//     resetCanvas();
//     localStorage.clear();
//     sizeLineGraph();
//     var ctx = document.getElementById('flowLine').getContext('2d');
//     myChart = new Chart(ctx, {
//         type: dayGraph.type,
//         data: {
//             labels: dayGraph.labels,
//             datasets: [{
//                 label: dayGraph.heading,
//                 data: dayGraph.data,
//                 backgroundColor: dayGraph.backgroundColor,
//                 borderColor: dayGraph.borderColor,
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             legend: {
//                 labels: {
//                     boxWidth: 0,
//                 }
//             },
//             scales: {
//                 yAxes: [{
//                     ticks: {
//                         beginAtZero: true
//                     }
//                 }]
//             }
//         }
//     });
// }

function generateWeekGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: weekGraph.type,
        data: {
            labels: weekGraph.labels,
            datasets: [{
                label: weekGraph.heading,
                data: weekGraph.data,
                backgroundColor: weekGraph.backgroundColor,
                borderColor: weekGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateMonthGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: monthGraph.type,
        data: {
            labels: monthGraph.labels,
            datasets: [{
                label: monthGraph.heading,
                data: monthGraph.data,
                backgroundColor: monthGraph.backgroundColor,
                borderColor: monthGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateThreeMonthGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: threeMonthGraph.type,
        data: {
            labels: threeMonthGraph.labels,
            datasets: [{
                label: threeMonthGraph.heading,
                data: threeMonthGraph.data,
                backgroundColor: threeMonthGraph.backgroundColor,
                borderColor: threeMonthGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateSixMonthGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: sixMonthGraph.type,
        data: {
            labels: sixMonthGraph.labels,
            datasets: [{
                label: sixMonthGraph.heading,
                data: sixMonthGraph.data,
                backgroundColor: sixMonthGraph.backgroundColor,
                borderColor: sixMonthGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateYearGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: yearGraph.type,
        data: {
            labels: yearGraph.labels,
            datasets: [{
                label: yearGraph.heading,
                data: yearGraph.data,
                backgroundColor: yearGraph.backgroundColor,
                borderColor: yearGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateThreeYearGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: threeYearGraph.type,
        data: {
            labels: threeYearGraph.labels,
            datasets: [{
                label: threeYearGraph.heading,
                data: threeYearGraph.data,
                backgroundColor: threeYearGraph.backgroundColor,
                borderColor: threeYearGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateFiveYearGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: fiveYearGraph.type,
        data: {
            labels: fiveYearGraph.labels,
            datasets: [{
                label: fiveYearGraph.heading,
                data: fiveYearGraph.data,
                backgroundColor: fiveYearGraph.backgroundColor,
                borderColor: fiveYearGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
        },
    });
}

//EXPENSE LINE CHARTS START////////////////////////////////////////////////////

// function generateDayExpenseGraph() {
//     resetCanvas();
//     localStorage.clear();
//     sizeLineGraph();
//     var ctx = document.getElementById('flowLine').getContext('2d');
//     myChart = new Chart(ctx, {
//         type: dayExpenseGraph.type,
//         data: {
//             labels: dayGraph.labels,
//             datasets: [{
//                 label: dayExpenseGraph.heading,
//                 data: dayExpenseGraph.data,
//                 backgroundColor: dayExpenseGraph.backgroundColor,
//                 borderColor: dayExpenseGraph.borderColor,
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             legend: {
//                 labels: {
//                     boxWidth: 0,
//                 }
//             },
//             scales: {
//                 yAxes: [{
//                     ticks: {
//                         beginAtZero: true
//                     }
//                 }]
//             }
//         }
//     });
// }

function generateWeekExpenseGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: weekExpenseGraph.type,
        data: {
            labels: weekExpenseGraph.labels,
            datasets: [{
                label: weekExpenseGraph.heading,
                data: weekExpenseGraph.data,
                backgroundColor: weekExpenseGraph.backgroundColor,
                borderColor: weekExpenseGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateMonthExpenseGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: monthExpenseGraph.type,
        data: {
            labels: monthExpenseGraph.labels,
            datasets: [{
                label: monthExpenseGraph.heading,
                data: monthExpenseGraph.data,
                backgroundColor: monthExpenseGraph.backgroundColor,
                borderColor: monthExpenseGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateThreeMonthExpenseGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: threeMonthExpenseGraph.type,
        data: {
            labels: threeMonthExpenseGraph.labels,
            datasets: [{
                label: threeMonthExpenseGraph.heading,
                data: threeMonthExpenseGraph.data,
                backgroundColor: threeMonthExpenseGraph.backgroundColor,
                borderColor: threeMonthExpenseGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateSixMonthExpenseGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: sixMonthGraph.type,
        data: {
            labels: sixMonthExpenseGraph.labels,
            datasets: [{
                label: sixMonthExpenseGraph.heading,
                data: sixMonthExpenseGraph.data,
                backgroundColor: sixMonthExpenseGraph.backgroundColor,
                borderColor: sixMonthExpenseGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateYearExpenseGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: yearExpenseGraph.type,
        data: {
            labels: yearExpenseGraph.labels,
            datasets: [{
                label: yearExpenseGraph.heading,
                data: yearExpenseGraph.data,
                backgroundColor: yearExpenseGraph.backgroundColor,
                borderColor: yearExpenseGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateThreeYearExpenseGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: threeYearExpenseGraph.type,
        data: {
            labels: threeYearExpenseGraph.labels,
            datasets: [{
                label: threeYearExpenseGraph.heading,
                data: threeYearExpenseGraph.data,
                backgroundColor: threeYearExpenseGraph.backgroundColor,
                borderColor: threeYearExpenseGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateFiveYearExpenseGraph() {
    resetCanvas();
    localStorage.clear();
    sizeLineGraph();
    var ctx = document.getElementById('flowLine').getContext('2d');
    var myChart = new Chart(ctx, {
        type: fiveYearExpenseGraph.type,
        data: {
            labels: fiveYearExpenseGraph.labels,
            datasets: [{
                label: fiveYearExpenseGraph.heading,
                data: fiveYearExpenseGraph.data,
                backgroundColor: fiveYearExpenseGraph.backgroundColor,
                borderColor: fiveYearExpenseGraph.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
        },
    });
}



///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
//          START SECONDARY GRAPH SECTION                      ////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//USER NEEDS TO BE ABLE TO CHOOSE BETWEEN BOTH PIE AND BAR GRAPHS IN THIS SECTION

/////////////////////////////////////////////////////////////////////////////////////
//          PIE/BAR CHARTS                                     //////////////////////
/////////////////////////////////////////////////////////////////////////////////////

//Class for Bar Charts
class barChart {
    constructor(type, labels, heading, data, backgroundColor, borderColor) {
        this.type = type;
        this.labels = labels,
            this.heading = heading,
            this.data = data;
        this.backgroundColor = backgroundColor;
        this.borderColor = borderColor;
    }
}

//Class for Pie Chart
class pieChart {
    constructor(type, labels, data, backgroundColor, borderColor) {
        this.type = type;
        this.labels = labels,
            this.data = data;
        this.backgroundColor = backgroundColor;
        this.borderColor = borderColor;
    }
}

var expenses, sales, payroll;

function getTotalExpenses() {
    var expenses = a.q;
    return expenses;
}

function getTotalIncome() {
    var income = a.r;
    return income;
}

function getOperatingExpenses() {
    var opExpenses = a.s;
    return opExpenses;
}


//Bar Chart Functions
function getTotalBarChartLabels() {
    var labels = ['Income', 'Expenses'];
    return labels;
}

function getTotalBarChartData() {
    var income, expenses, data;
    income = getTotalIncome();
    expenses = getTotalExpenses();
    data = [income, expenses];
    return data;
}

function getTotalBarChartHeading() {
    var heading = 'Totals';
    return heading;
}

function getTotalBarChartBackgroundColor() {
    var colors = ['rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)'
    ];
    return colors;
}

function getTotalBarChartBorderColor() {
    var colors = ['rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)'
    ];
    return colors;
}

function getIncomeBarChartLabels() {
    var labels = ['Sales', 'Services', 'Other'];
    return labels;
}

function getincomeBarChartData() {
    var income = a.t;
    return income;
}

function getIncomeBarChartHeading() {
    var heading = 'Income';
    return heading;
}

function getIncomeBarChartBackgroundColor() {
    var colors = ['rgba(25, 99, 132, 1)',
        'rgba(54, 162, 23, 1)',
        'rgba(13, 55, 209, 1)'
    ];
    return colors;
}

function getIncomeBarChartBorderColor() {
    var colors = ['rgba(255, 99, 132, 1)',
        'rgba(24, 162, 95, 1)',
        'rgba(101, 49, 253, 1)'
    ];
    return colors;
}

function getExpenseBarChartLabels() {
    var labels = ['Utilities', 'Payroll', 'Advertising Costs', 'Other'];
    return labels;
}

function getExpenseBarChartData() {
    data = a.u;
    return data;
}

function getExpenseBarChartHeading() {
    var heading = 'Expenses';
    return heading;
}

function getExpenseBarChartBackgroundColor() {
    var colors = ['rgba(25, 99, 232, 1)',
        'rgba(124, 12, 195, 1)',
        'rgba(25, 199, 232, 1)',
        'rgba(24, 12, 95, 1)',
        'rgba(250, 19, 232, 1)'
    ];
    return colors;
}

function getExpenseBarChartBorderColor() {
    var colors = ['rgba(253, 199, 232, 1)',
        'rgba(124, 212, 95, 1)',
        'rgba(23, 199, 32, 1)',
        'rgba(24, 212, 195, 1)',
        'rgba(53, 144, 32, 1)'
    ];
    return colors;
}


//Create Objects for Bar Charts
var totalBarChart, totalBarChartType, totalBarChartLabels, totalBarChartData, totalBarChartHeading, totalBarChartBackgroundColor, totalBarChartBorderColor;
totalBarChartType = 'bar';
totalBarChartLabels = getTotalBarChartLabels();
totalBarChartData = getTotalBarChartData();
totalBarChartHeading = getTotalBarChartHeading();
totalBarChartBackgroundColor = getTotalBarChartBackgroundColor();
totalBarChartBorderColor = getTotalBarChartBorderColor();

totalBarChart = new barChart(totalBarChartType, totalBarChartLabels, totalBarChartHeading, totalBarChartData, totalBarChartBackgroundColor, totalBarChartBorderColor);

var expenseBarChart, expenseBarChartType, expenseBarChartLabels, expenseBarChartData, expenseBarChartHeading, expenseBarChartBackgroundColor, expenseBarChartBorderColor;
expenseBarChartType = 'bar';
expenseBarChartLabels = getExpenseBarChartLabels();
expenseBarChartData = getExpenseBarChartData();
expenseBarChartHeading = getExpenseBarChartHeading();
expenseBarChartBackgroundColor = getExpenseBarChartBackgroundColor();
expenseBarChartBorderColor = getExpenseBarChartBorderColor();

expenseBarChart = new barChart(expenseBarChartType, expenseBarChartLabels, expenseBarChartHeading, expenseBarChartData, expenseBarChartBackgroundColor, expenseBarChartBorderColor);

var incomeBarChart, incomeBarChartType, incomeBarChartLabels, incomeBarChartData, incomeBarChartHeading, incomeBarChartBackgroundColor, incomeBarChartBorderColor;
incomeBarChartType = 'bar';
incomeBarChartLabels = getIncomeBarChartLabels();
incomeBarChartData = getincomeBarChartData();
incomeBarChartHeading = getIncomeBarChartHeading();
incomeBarChartBackgroundColor = getIncomeBarChartBackgroundColor();
incomeBarChartBorderColor = getIncomeBarChartBorderColor();

incomeBarChart = new barChart(incomeBarChartType, incomeBarChartLabels, incomeBarChartHeading, incomeBarChartData, incomeBarChartBackgroundColor, incomeBarChartBorderColor);

//Create Objects/Parameters for Pie Charts
var totalPieChart, expensePieChart, incomePieChart;
totalPieChart = new pieChart('pie', totalBarChartLabels, totalBarChartData, totalBarChartBackgroundColor, totalBarChartBorderColor);
expensePieChart = new pieChart('pie', expenseBarChart.labels, expenseBarChart.data, expenseBarChart.backgroundColor, expenseBarChart.borderColor);
incomePieChart = new pieChart('pie', incomeBarChart.labels, incomeBarChart.data, incomeBarChart.backgroundColor, incomeBarChart.borderColor);
//^^^^^ LEECHING FROM PRIOR DATA WITHIN THE BAR CHARTS SECTION TO FILL PIE CHART////////

/////////////////////////////////////////////////////////////////////////////////////
//          BELOW GENERATES THE PIE CHARTS                     //////////////////////
/////////////////////////////////////////////////////////////////////////////////////
var currentChart;

function resetPieCanvas() { //FIXES ONHOVER GLITCH WHERE IT JUMPS BETWEEN PRIOR GRAPHS
    $('#flowPie').remove();
    $('#pieChartSection').append('<canvas id="flowPie"><canvas>');
    canvas = document.querySelector('#flowPie');
    ctx = canvas.getContext('2d');
    sizePieGraph();
};

function generateTotalPieChart() {
    resetPieCanvas();
    currentChart = totalPieChart;
    localStorage.clear();
    sizePieGraph();
    var ctx = document.getElementById('flowPie').getContext('2d');
    myChart = new Chart(ctx, {
        type: totalPieChart.type,
        data: {
            labels: totalPieChart.labels,
            datasets: [{
                data: totalPieChart.data,
                backgroundColor: totalPieChart.backgroundColor,
                borderColor: totalPieChart.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Fiscal YTD'
            }
        }
    });
}

function generateIncomePieChart() {
    resetPieCanvas();
    currentChart = incomePieChart;
    localStorage.clear();
    sizePieGraph();
    var ctx = document.getElementById('flowPie').getContext('2d');
    myChart = new Chart(ctx, {
        type: incomePieChart.type,
        data: {
            labels: incomePieChart.labels,
            datasets: [{
                data: incomePieChart.data,
                backgroundColor: incomePieChart.backgroundColor,
                borderColor: incomePieChart.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Fiscal Income'
            }
        }
    });
}

function generateExpensePieChart() {
    resetPieCanvas();
    currentChart = expensePieChart;
    localStorage.clear();
    sizePieGraph();
    var ctx = document.getElementById('flowPie').getContext('2d');
    myChart = new Chart(ctx, {
        type: expensePieChart.type,
        data: {
            labels: expensePieChart.labels,
            datasets: [{
                data: expensePieChart.data,
                backgroundColor: expensePieChart.backgroundColor,
                borderColor: expensePieChart.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Fiscal Expenses'
            }
        }
    });
}
/////////////////////////////////////////////////////////////////////////////////////
//          BELOW GENERATES THE BAR CHARTS                      /////////////////////
/////////////////////////////////////////////////////////////////////////////////////
function generateTotalBarChart() {
    resetPieCanvas();
    currentChart = totalBarChart;
    localStorage.clear();
    sizePieGraph();
    var ctx = document.getElementById('flowPie').getContext('2d');
    myChart = new Chart(ctx, {
        type: totalBarChart.type,
        data: {
            labels: totalBarChart.labels,
            datasets: [{
                label: totalBarChart.heading,
                data: totalBarChart.data,
                backgroundColor: totalBarChart.backgroundColor,
                borderColor: totalBarChart.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateIncomeBarChart() {
    resetPieCanvas();
    currentChart = incomeBarChart;
    localStorage.clear();
    sizePieGraph();
    var ctx = document.getElementById('flowPie').getContext('2d');
    myChart = new Chart(ctx, {
        type: incomeBarChart.type,
        data: {
            labels: incomeBarChart.labels,
            datasets: [{
                label: incomeBarChart.heading,
                data: incomeBarChart.data,
                backgroundColor: incomeBarChart.backgroundColor,
                borderColor: incomeBarChart.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function generateExpenseBarChart() {
    resetPieCanvas();
    currentChart = expenseBarChart;
    localStorage.clear();
    sizePieGraph();
    var ctx = document.getElementById('flowPie').getContext('2d');
    myChart = new Chart(ctx, {
        type: expenseBarChart.type,
        data: {
            labels: expenseBarChart.labels,
            datasets: [{
                label: expenseBarChart.heading,
                data: expenseBarChart.data,
                backgroundColor: expenseBarChart.backgroundColor,
                borderColor: expenseBarChart.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                labels: {
                    boxWidth: 0,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

//Finally, the ability for the user to swap back and forth between pie and bar charts
function pieCharts() {
    var pieChartSection, lineChartSection, pieChartButtons, lineChartButtons, pieSwap, lineSwap, lineDataType, lineChartExpenseOptions;
    pieChartSection = document.getElementById('pieChartSection');
    lineChartSection = document.getElementById('lineChartSection');
    pieChartButtons = document.getElementById('pieChartButtons');
    lineChartButtons = document.getElementById('lineChartButtons');
    pieSwap = document.getElementById('pieSwap');
    lineSwap = document.getElementById('lineSwap');
    lineDataType = document.getElementById('LineChartsChange');
    lineChartExpenseOptions = document.getElementById('lineChartButtonsExpense');

    pieChartSection.style.display = 'block';
    pieChartButtons.style.display = 'block';
    pieSwap.style.display = 'none';

    lineChartSection.style.display = 'none';
    lineChartButtons.style.display = 'none';
    lineDataType.style.display = 'none';
    lineChartExpenseOptions.style.display = 'none';
    lineSwap.style.display = 'block';

    generateTotalPieChart();
}

function lineCharts() {
    var pieChartSection, lineChartSection, pieChartButtons, lineChartButtons, pieSwap, lineSwap, lineDataType, lineChartExpenseOptions;
    pieChartSection = document.getElementById('pieChartSection');
    lineChartSection = document.getElementById('lineChartSection');
    pieChartButtons = document.getElementById('pieChartButtons');
    lineChartButtons = document.getElementById('lineChartButtons');
    pieSwap = document.getElementById('pieSwap');
    lineSwap = document.getElementById('lineSwap');
    lineDataType = document.getElementById('LineChartsChange');
    lineChartExpenseOptions = document.getElementById('lineChartButtonsExpense');

    pieChartSection.style.display = 'none';
    pieChartButtons.style.display = 'none';
    pieSwap.style.display = 'block';

    lineChartSection.style.display = 'block';
    lineChartButtons.style.display = 'block';
    lineChartExpenseOptions.style.display = 'none';
    lineDataType.style.display = 'block';
    lineSwap.style.display = 'none';

    generateWeekGraph();
}

//For swapping between Revenue and Expense Line Charts

function expenseLineCharts(){
    var lineChartOptions, lineChartExpenseOptions;

    lineChartExpenseOptions = document.getElementById('lineChartButtonsExpense');
    lineChartOptions = document.getElementById('lineChartButtons');

    lineChartExpenseOptions.style.display = 'block';
    lineChartOptions.style.display = 'none';

    generateWeekExpenseGraph();
}

function revenueLineCharts(){
    var lineChartOptions, lineChartExpenseOptions;

    lineChartExpenseOptions = document.getElementById('lineChartButtonsExpense');
    lineChartOptions = document.getElementById('lineChartButtons');

    lineChartExpenseOptions.style.display = 'none';
    lineChartOptions.style.display = 'block';

    generateWeekGraph();
}