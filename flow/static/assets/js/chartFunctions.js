function monthSet() {
    monthArray = [];
    for (i = 0; i < 31; i++) {
        monthArray.push("'" + i + "'");
    }
    return monthArray;
}