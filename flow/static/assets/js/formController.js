function showCustomerForm(){
    document.getElementById('customerForm').style.display = 'block';
    document.getElementById('vendorForm').style.display = 'none';
    document.getElementById('entrySelector').style.display = 'none';
}

function showVendorForm(){
    document.getElementById('customerForm').style.display = 'none';
    document.getElementById('vendorForm').style.display = 'block';
    document.getElementById('entrySelector').style.display = 'none';
}