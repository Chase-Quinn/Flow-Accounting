function writeDate() {
    date = new Date();
    document.write(date);
    function writeDate() {
        date = new Date();
        document.getElementById('dateTime').innerHTML = date;
    }
    setInterval(writeDate, 1000);
}

function fillOverviewTooltip() {
    document.write(overview);
}

function pageRefresh() {
    location.reload();
}

function pageBack() {
    window.history.back();
}

function printPage(contents) {
    var printContents = document.getElementById(contents).innerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;

    window.print();

    document.body.innerHTML = originalContents;
}