// owl carousel slider js
$('.team_carousel').owlCarousel({
    loop: true,
    margin: 15,
    dots: true,
    autoplay: true,
    navText: [
        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
    ],
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1,
            margin: 0
        },
        576: {
            items: 2,
        },
        992: {
            items: 3
        }
    }
});
// **************************** Siam Aisin ***************************************

document.getElementById("Uploadbutton_fcc").onclick = function() {
    document.getElementById('fileInput_fcc').click();
    // Clear text file/CSV file to prevent import empty
    document.getElementById('filepath_fcc').innerHTML = "No file selected.";
    // Default value for upload data
    document.getElementById('soldto_fcc').value = "CL203700";
    document.getElementById('shipto_fcc').value = "CL203700";
    document.getElementById('site_fcc').value = "423";
    document.getElementById('taxclass_fcc').value = "42V";
    document.getElementById('PriceTbl_fcc').value = "CL203700";
};    
document.getElementById('fileInput_fcc').onchange = function() {
    document.getElementById('filepath_fcc').innerHTML = this.files[0].name;
};

// Clear data when form hidden
$('#TransferModal_fcc').on('hidden.bs.modal', function() {
    $('#uploadForm_fcc')[0].reset();
});
$('#SOrunningModal_fcc').on('hidden.bs.modal', function() {
    $('#sorunningForm_fcc')[0].reset();
});
$('#CIMcreateModal_fcc').on('hidden.bs.modal', function() {
    $('#cimcreateForm_fcc')[0].reset();
});

//CIM create download button handle
const fcc_fileCIM = document.getElementById('outputfile_fcc');
const fcc_exportBtn = document.getElementById('Downloadbutton_fcc');

// Clear sales order function
var clearsoForm_fcc = document.getElementById('clearsoForm_fcc');
clearsoForm_fcc.addEventListener('submit', function(event) {
    event.preventDefault();

    var clearsoredirect_fcc = document.getElementById('clear_so_url_fcc').value;
    
    let clearsoMessage_fcc = document.getElementById('clearOrderMessage_fcc');
    fetch(clearsoredirect_fcc, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            clearsoMessage_fcc.classList.toggle("alert-success");
            clearsoMessage_fcc.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = clearsoredirect_fcc.substring(0, clearsoredirect_fcc.lastIndexOf('/'));
            }, 3000);
        } else {
            clearsoMessage_fcc.classList.toggle("alert-danger");
            clearsoMessage_fcc.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        clearsoMessage_fcc.classList.toggle("alert-danger");
        clearsoMessage_fcc.textContent = "Error: Could not clear sales order.";
        console.error(error);
    });
});

// Clear data function
var cleardataForm_fcc = document.getElementById('cleardataForm_fcc');
cleardataForm_fcc.addEventListener('submit', function(event) {
    event.preventDefault();

    var cleardataredirect_fcc = document.getElementById('clear_data_fcc').value;
    $('#cleardata_submit_fcc').attr('disabled','disabled');
    
    let clearDataMessage = document.getElementById('cleardataMessage_fcc');
    fetch(cleardataredirect_fcc, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            clearDataMessage.classList.remove("alert-danger");
            clearDataMessage.classList.add("alert-success");
            clearDataMessage.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = cleardataredirect_fcc.substring(0, cleardataredirect_fcc.lastIndexOf('/'));
            }, 2000);
        } else {
            $('#cleardata_submit_fcc').removeAttr('disabled');
            clearDataMessage.classList.remove("alert-success");
            clearDataMessage.classList.add("alert-danger");
            clearDataMessage.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        $('#cleardata_submit_fcc').removeAttr('disabled');
        clearDataMessage.classList.remove("alert-success");
        clearDataMessage.classList.add("alert-danger");
        clearDataMessage.textContent = "Error: Could not clear data.";
        console.error(error);
    });
});

// Sales order running function
var sorunningForm_fcc = document.getElementById('sorunningForm_fcc');
sorunningForm_fcc.addEventListener('submit', function(event) {
    event.preventDefault();

    var formSalesOrder_fcc = new FormData();
    var runningredirect_fcc = document.getElementById('sorunning_url_fcc').value;
    var elements = sorunningForm_fcc.elements;
    for(var i = 0; i < elements.length; i++) {
        var item = elements.item(i);
        formSalesOrder_fcc.append(item.name, item.value);
    }

    let salesorderMessage_fcc = document.getElementById('salesOrderMessage_fcc');
    fetch(runningredirect_fcc, {
        method: 'POST',
        body: formSalesOrder_fcc
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success) {
            salesorderMessage_fcc.classList.toggle("alert-success");
            salesorderMessage_fcc.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = runningredirect_fcc.substring(0, runningredirect_fcc.lastIndexOf('/'));
            }, 3000);
        } else {
            salesorderMessage_fcc.classList.toggle("alert-danger");
            salesorderMessage_fcc.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        salesorderMessage_fcc.classList.toggle("alert-danger");
        salesorderMessage_fcc.textContent = "Error: Could not running sales order.";
        console.error(error);
    });
});

//CIM Create function
var cimcreateForm_fcc = document.getElementById('cimcreateForm_fcc');
var buttonClicked_fcc = '';
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners here
    var exportButton_fcc = document.querySelector('input[name="export"]');
    var okButton_fcc = document.querySelector('button[name="ok"]');
    
    if (exportButton_fcc) {
        exportButton_fcc.addEventListener('click', function() {
            buttonClicked_fcc = 'export';
        });
    }
    
    if (okButton_fcc) {
        okButton_fcc.addEventListener('click', function() {
            buttonClicked_fcc = 'ok';
        });
    }
});
cimcreateForm_fcc.addEventListener('submit', function(event) {
    event.preventDefault();

    var formCreate_fcc = new FormData();
    var createurl_fcc = document.getElementById('cim_create_url_fcc').value;
    var filename_fcc = document.getElementById('outputfile_fcc').value;
    
    var elements = cimcreateForm_fcc.elements;

    for(var i=0; i < elements.length; i++) {
        var item = elements.item(i);
        formCreate_fcc.append(item.name, item.value);
    }

    let createMessage_fcc = document.getElementById('cim_create_message_fcc');

    if (buttonClicked_fcc === 'ok') {
        // Specific behavior for the "OK" button
        console.log("OK button pressed. Performing OK-specific action...");
        formCreate_fcc.delete("export")
        // You can modify createurl_fcc or other parameters as needed for the "OK" action
    } else if (buttonClicked_fcc === 'export') {
        // Specific behavior for the "export" button
        console.log("Export button pressed. Performing export-specific action...");
        formCreate_fcc.delete("ok")
    }

    fetch(createurl_fcc, {
        method: 'POST',
        body: formCreate_fcc
    })
    // .then(response => response.json())
    .then(response => {
        // Check the content type of the response
        const contentType = response.headers.get('content-type');
        console.log(contentType);
        if (contentType.includes('application/json')) {
            return response.json(); // Parse as JSON
        } else if (contentType.includes('application/octet-stream') || contentType.includes('attachment')) {
            return response.blob(); // Parse as a Blob for file download
        } else {
            throw new Error("Unexpected content type: " + contentType);
        }
    })
    .then(data => {
        // Handle normal json (CIM and FTP)
        if (data instanceof Object && data.success != undefined) {
            if (data.success) {
                console.log(data.success)
                createMessage_fcc.classList.remove("alert-danger");
                createMessage_fcc.classList.add("alert-success");
                createMessage_fcc.textContent = data.message;
                setTimeout (function () {
                    window.location.href = createurl_fcc.substring(0, createurl_fcc.lastIndexOf('/'));
                }, 3000);
            } else {
                createMessage_fcc.classList.remove("alert-success");
                createMessage_fcc.classList.add("alert-danger");
                createMessage_fcc.textContent = "Error: " + data.message;
            }
        } else if (data instanceof Blob) {
            // Try to export data
            const url = window.URL.createObjectURL(data);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename_fcc + '.cim';
            document.body.appendChild(a);
            a.click();
            a.remove();
        }
    })
    .catch(error => {
        // Handle any errors
        createMessage_fcc.classList.remove("alert-success");
        createMessage_fcc.classList.add("alert-danger");
        createMessage_fcc.textContent = "Error: Could not create CIM file.";
        console.error(error);
    });
});

// Transfer function
var transferForm_fcc = document.getElementById('uploadForm_fcc');
transferForm_fcc.addEventListener('submit', function(event) {
    event.preventDefault();

    // Disable the submit button to prevent duplicate submissions
    $('#transfer_submit_fcc').attr('disabled','disabled');
    transferForm_fcc.setAttribute('data-sending','true');

    // Create a FormData object to hold the uploaded file
    var formData_fcc = new FormData();
    var fileInput_fcc = document.getElementById('fileInput_fcc');
    var redirecturl_fcc = document.getElementById('redirecturl_fcc').value;
    formData_fcc.append('file', fileInput_fcc.files[0]);
    var elements = transferForm_fcc.elements;
    // var obj ={};
    for(var i = 0; i < elements.length; i++){
        var item = elements.item(i);
        // obj[item.name] = item.value;
        formData_fcc.append(item.name, item.value);
    }

    let statusMessage_fcc = document.getElementById('uploadMessage_fcc');

    // Use fetch to send the form data to the server via POST
    fetch(redirecturl_fcc, {
        method: 'POST',
        body: formData_fcc
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        // Update the status message based on the server response
        if (data.success) {
            statusMessage_fcc.classList.remove("alert-danger");
            statusMessage_fcc.classList.add("alert-success");
            statusMessage_fcc.textContent = "File uploaded and data updated successfully!";
            setTimeout (function () {
                window.location.href = redirecturl_fcc.substring(0, redirecturl_fcc.lastIndexOf('/'));
            }, 2000);
        } else {
            $('#transfer_submit_fcc').removeAttr('disabled');
            statusMessage_fcc.classList.remove("alert-success");
            statusMessage_fcc.classList.add("alert-danger");
            statusMessage_fcc.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        $('#transfer_submit_fcc').removeAttr('disabled');
        statusMessage_fcc.classList.remove("alert-success");
        statusMessage_fcc.classList.add("alert-danger");
        statusMessage_fcc.textContent = "Error: Could not upload file.";
        console.error(error);
    });
});

function validatetransferForm_fcc() {
    const soldto = document.forms["uploadForm_fcc"]["soldto_fcc"].value.trim();
    const shipto = document.forms["uploadForm_fcc"]["shipto_fcc"].value.trim();
    const site = document.forms["uploadForm_fcc"]["site_fcc"].value.trim();
    const taxclass = document.forms["uploadForm_fcc"]["taxclass_fcc"].value.trim();
    const pritable = document.forms["uploadForm_fcc"]["PriceTbl_fcc"].value.trim();

    if (soldto === "" || shipto === "" || site === "" || taxclass === "" || pritable === "") {
        alert("All fields must be filled out and should not contain only spaces.");
        console.log("false");
        return false;
    }
    return true;
};

// adjust for table style (8 records per page) 
const rows_fcc = document.querySelectorAll('.table-row');
const rowsPerPage_fcc = 7;
let currentPage_fcc = 1;

function showPage_fcc(page) {
    const start = (page - 1) * rowsPerPage_fcc;
    const end = start + rowsPerPage_fcc;

    //Hide all rows
    rows_fcc.forEach(row => row.style.display = 'none');

    //Show thr rows only current page
    rows_fcc.forEach((row, index) => {
        if (index >= start && index < end) {
            row.style.display = 'table-row';
        }
    });

    var totalPage = Math.ceil(rows_fcc.length / rowsPerPage_fcc);
    if (totalPage === 0) {
        totalPage = 1;
    };

    document.getElementById('page-info_fcc').textContent = `Page ${page} of ${totalPage}`;
    document.getElementById('prev-btn_fcc').classList.toggle('disabled', page === 1);
    document.getElementById('next-btn_fcc').classList.toggle('disabled', page === totalPage);
};

// Initial call to display the first page
showPage_fcc(currentPage_fcc);

// Previous button
document.getElementById('prev-btn_fcc').addEventListener('click', function() {
    if (currentPage_fcc > 1) {
        currentPage_fcc--;
        showPage_fcc(currentPage_fcc);
    }
});
// Next button
document.getElementById('next-btn_fcc').addEventListener('click', function() {
    if (currentPage_fcc < Math.ceil(rows_fcc.length / rowsPerPage_fcc)) {
        currentPage_fcc++;
        showPage_fcc(currentPage_fcc);
    }
});

// **************************** Siam Aisin ***************************************
// **************************** Siam Aisin ***************************************

document.getElementById("Uploadbutton_siam_aisin").onclick = function() {
    console.log("Test");
    document.getElementById('fileInput_siam_aisin').click();
    // Clear text file/CSV file to prevent import empty
    document.getElementById('filepath_siam_aisin').innerHTML = "No file selected.";
    // Default value for upload data
    document.getElementById('soldto_siam_aisin').value = "CL203700";
    document.getElementById('shipto_siam_aisin').value = "CL203700";
    document.getElementById('site_siam_aisin').value = "423";
    document.getElementById('taxclass_siam_aisin').value = "42V";
    document.getElementById('PriceTbl_siam_aisin').value = "CL203700";
};    
document.getElementById('fileInput_siam_aisin').onchange = function() {
    document.getElementById('filepath_siam_aisin').innerHTML = this.files[0].name;
};

// Clear data when form hidden
$('#TransferModal_siam_aisin').on('hidden.bs.modal', function() {
    $('#uploadForm_siam_aisin')[0].reset();
});
$('#SOrunningModal_siam_aisin').on('hidden.bs.modal', function() {
    $('#sorunningForm_siam_aisin')[0].reset();
});
$('#CIMcreateModal_siam_aisin').on('hidden.bs.modal', function() {
    $('#cimcreateForm_siam_aisin')[0].reset();
});

//CIM create download button handle
const siam_aisin_fileCIM = document.getElementById('outputfile_siam_aisin');
const siam_aisin_exportBtn = document.getElementById('Downloadbutton_siam_aisin');

// Clear sales order function
var clearsoForm_siam_aisin = document.getElementById('clearsoForm_siam_aisin');
clearsoForm_siam_aisin.addEventListener('submit', function(event) {
    event.preventDefault();

    var clearsoredirect_siam_aisin = document.getElementById('clear_so_url_siam_aisin').value;
    
    let clearsoMessage_siam_aisin = document.getElementById('clearOrderMessage_siam_aisin');
    fetch(clearsoredirect_siam_aisin, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            clearsoMessage_siam_aisin.classList.toggle("alert-success");
            clearsoMessage_siam_aisin.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = clearsoredirect_siam_aisin.substring(0, clearsoredirect_siam_aisin.lastIndexOf('/'));
            }, 3000);
        } else {
            clearsoMessage_siam_aisin.classList.toggle("alert-danger");
            clearsoMessage_siam_aisin.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        clearsoMessage_siam_aisin.classList.toggle("alert-danger");
        clearsoMessage_siam_aisin.textContent = "Error: Could not clear sales order.";
        console.error(error);
    });
});

// Clear data function
var cleardataForm_siam_aisin = document.getElementById('cleardataForm_siam_aisin');
cleardataForm_siam_aisin.addEventListener('submit', function(event) {
    event.preventDefault();
    console.log("Here");

    var cleardataredirect_siam_aisin = document.getElementById('clear_data_siam_aisin').value;
    $('#cleardata_submit_siam_aisin').attr('disabled','disabled');
    
    let clearDataMessage = document.getElementById('cleardataMessage_siam_aisin');
    fetch(cleardataredirect_siam_aisin, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            clearDataMessage.classList.remove("alert-danger");
            clearDataMessage.classList.add("alert-success");
            clearDataMessage.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = cleardataredirect_siam_aisin.substring(0, cleardataredirect_siam_aisin.lastIndexOf('/'));
            }, 2000);
        } else {
            $('#cleardata_submit_siam_aisin').removeAttr('disabled');
            clearDataMessage.classList.remove("alert-success");
            clearDataMessage.classList.add("alert-danger");
            clearDataMessage.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        $('#cleardata_submit_siam_aisin').removeAttr('disabled');
        clearDataMessage.classList.remove("alert-success");
        clearDataMessage.classList.add("alert-danger");
        clearDataMessage.textContent = "Error: Could not clear data.";
        console.error(error);
    });
});

// Sales order running function
var sorunningForm_siam_aisin = document.getElementById('sorunningForm_siam_aisin');
sorunningForm_siam_aisin.addEventListener('submit', function(event) {
    event.preventDefault();

    var formSalesOrder_siam_aisin = new FormData();
    var runningredirect_siam_aisin = document.getElementById('sorunning_url_siam_aisin').value;
    var elements = sorunningForm_siam_aisin.elements;
    for(var i = 0; i < elements.length; i++) {
        var item = elements.item(i);
        formSalesOrder_siam_aisin.append(item.name, item.value);
    }

    let salesorderMessage_siam_aisin = document.getElementById('salesOrderMessage_siam_aisin');
    fetch(runningredirect_siam_aisin, {
        method: 'POST',
        body: formSalesOrder_siam_aisin
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success) {
            salesorderMessage_siam_aisin.classList.toggle("alert-success");
            salesorderMessage_siam_aisin.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = runningredirect_siam_aisin.substring(0, runningredirect_siam_aisin.lastIndexOf('/'));
            }, 3000);
        } else {
            salesorderMessage_siam_aisin.classList.toggle("alert-danger");
            salesorderMessage_siam_aisin.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        salesorderMessage_siam_aisin.classList.toggle("alert-danger");
        salesorderMessage_siam_aisin.textContent = "Error: Could not running sales order.";
        console.error(error);
    });
});

//CIM Create function
var cimcreateForm_siam_aisin = document.getElementById('cimcreateForm_siam_aisin');
var buttonClicked_siam_aisin = '';
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners here
    var exportButton_siam_aisin = document.querySelector('input[name="export"]');
    var okButton_siam_aisin = document.querySelector('button[name="ok"]');
    
    if (exportButton_siam_aisin) {
        exportButton_siam_aisin.addEventListener('click', function() {
            buttonClicked_siam_aisin = 'export';
        });
    }
    
    if (okButton_siam_aisin) {
        okButton_siam_aisin.addEventListener('click', function() {
            buttonClicked_siam_aisin = 'ok';
        });
    }
});
cimcreateForm_siam_aisin.addEventListener('submit', function(event) {
    event.preventDefault();

    var formCreate_siam_aisin = new FormData();
    var createurl_siam_aisin = document.getElementById('cim_create_url_siam_aisin').value;
    var filename_siam_aisin = document.getElementById('outputfile_siam_aisin').value;
    
    var elements = cimcreateForm_siam_aisin.elements;

    for(var i=0; i < elements.length; i++) {
        var item = elements.item(i);
        formCreate_siam_aisin.append(item.name, item.value);
    }

    let createMessage_siam_aisin = document.getElementById('cim_create_message_siam_aisin');

    if (buttonClicked_siam_aisin === 'ok') {
        // Specific behavior for the "OK" button
        console.log("OK button pressed. Performing OK-specific action...");
        formCreate_siam_aisin.delete("export")
        // You can modify createurl_siam_aisin or other parameters as needed for the "OK" action
    } else if (buttonClicked_siam_aisin === 'export') {
        // Specific behavior for the "export" button
        console.log("Export button pressed. Performing export-specific action...");
        formCreate_siam_aisin.delete("ok")
    }

    fetch(createurl_siam_aisin, {
        method: 'POST',
        body: formCreate_siam_aisin
    })
    // .then(response => response.json())
    .then(response => {
        // Check the content type of the response
        const contentType = response.headers.get('content-type');
        console.log(contentType);
        if (contentType.includes('application/json')) {
            return response.json(); // Parse as JSON
        } else if (contentType.includes('application/octet-stream') || contentType.includes('attachment')) {
            return response.blob(); // Parse as a Blob for file download
        } else {
            throw new Error("Unexpected content type: " + contentType);
        }
    })
    .then(data => {
        // Handle normal json (CIM and FTP)
        if (data instanceof Object && data.success != undefined) {
            if (data.success) {
                console.log(data.success)
                createMessage_siam_aisin.classList.remove("alert-danger");
                createMessage_siam_aisin.classList.add("alert-success");
                createMessage_siam_aisin.textContent = data.message;
                setTimeout (function () {
                    window.location.href = createurl_siam_aisin.substring(0, createurl_siam_aisin.lastIndexOf('/'));
                }, 3000);
            } else {
                createMessage_siam_aisin.classList.remove("alert-success");
                createMessage_siam_aisin.classList.add("alert-danger");
                createMessage_siam_aisin.textContent = "Error: " + data.message;
            }
        } else if (data instanceof Blob) {
            // Try to export data
            const url = window.URL.createObjectURL(data);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename_siam_aisin + '.cim';
            document.body.appendChild(a);
            a.click();
            a.remove();
        }
    })
    .catch(error => {
        // Handle any errors
        createMessage_siam_aisin.classList.remove("alert-success");
        createMessage_siam_aisin.classList.add("alert-danger");
        createMessage_siam_aisin.textContent = "Error: Could not create CIM file.";
        console.error(error);
    });
});

// Transfer function
var transferForm_siam_aisin = document.getElementById('uploadForm_siam_aisin');
transferForm_siam_aisin.addEventListener('submit', function(event) {
    event.preventDefault();

    // Disable the submit button to prevent duplicate submissions
    $('#transfer_submit_siam_aisin').attr('disabled','disabled');
    transferForm_siam_aisin.setAttribute('data-sending','true');

    // Create a FormData object to hold the uploaded file
    var formData_siam_aisin = new FormData();
    var fileInput_siam_aisin = document.getElementById('fileInput_siam_aisin');
    var redirecturl_siam_aisin = document.getElementById('redirecturl_siam_aisin').value;
    formData_siam_aisin.append('file', fileInput_siam_aisin.files[0]);
    var elements = transferForm_siam_aisin.elements;
    // var obj ={};
    for(var i = 0; i < elements.length; i++){
        var item = elements.item(i);
        // obj[item.name] = item.value;
        formData_siam_aisin.append(item.name, item.value);
    }

    let statusMessage_siam_aisin = document.getElementById('uploadMessage_siam_aisin');

    // Use fetch to send the form data to the server via POST
    fetch(redirecturl_siam_aisin, {
        method: 'POST',
        body: formData_siam_aisin
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        // Update the status message based on the server response
        if (data.success) {
            statusMessage_siam_aisin.classList.remove("alert-danger");
            statusMessage_siam_aisin.classList.add("alert-success");
            statusMessage_siam_aisin.textContent = "File uploaded and data updated successfully!";
            setTimeout (function () {
                window.location.href = redirecturl_siam_aisin.substring(0, redirecturl_siam_aisin.lastIndexOf('/'));
            }, 2000);
        } else {
            $('#transfer_submit_siam_aisin').removeAttr('disabled');
            statusMessage_siam_aisin.classList.remove("alert-success");
            statusMessage_siam_aisin.classList.add("alert-danger");
            statusMessage_siam_aisin.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        $('#transfer_submit_siam_aisin').removeAttr('disabled');
        statusMessage_siam_aisin.classList.remove("alert-success");
        statusMessage_siam_aisin.classList.add("alert-danger");
        statusMessage_siam_aisin.textContent = "Error: Could not upload file.";
        console.error(error);
    });
});

function validatetransferForm_siam_aisin() {
    const soldto = document.forms["uploadForm_siam_aisin"]["soldto_siam_aisin"].value.trim();
    const shipto = document.forms["uploadForm_siam_aisin"]["shipto_siam_aisin"].value.trim();
    const site = document.forms["uploadForm_siam_aisin"]["site_siam_aisin"].value.trim();
    const taxclass = document.forms["uploadForm_siam_aisin"]["taxclass_siam_aisin"].value.trim();
    const pritable = document.forms["uploadForm_siam_aisin"]["PriceTbl_siam_aisin"].value.trim();

    if (soldto === "" || shipto === "" || site === "" || taxclass === "" || pritable === "") {
        alert("All fields must be filled out and should not contain only spaces.");
        console.log("false");
        return false;
    }
    return true;
};

// adjust for table style (8 records per page) 
const rows_siam_aisin = document.querySelectorAll('.table-row');
const rowsPerPage_siam_aisin = 7;
let currentPage_siam_aisin = 1;

function showPage_siam_aisin(page) {
    const start = (page - 1) * rowsPerPage_siam_aisin;
    const end = start + rowsPerPage_siam_aisin;

    //Hide all rows
    rows_siam_aisin.forEach(row => row.style.display = 'none');

    //Show thr rows only current page
    rows_siam_aisin.forEach((row, index) => {
        if (index >= start && index < end) {
            row.style.display = 'table-row';
        }
    });

    var totalPage = Math.ceil(rows_siam_aisin.length / rowsPerPage_siam_aisin);
    if (totalPage === 0) {
        totalPage = 1;
    };

    document.getElementById('page-info_siam_aisin').textContent = `Page ${page} of ${totalPage}`;
    document.getElementById('prev-btn_siam_aisin').classList.toggle('disabled', page === 1);
    document.getElementById('next-btn_siam_aisin').classList.toggle('disabled', page === totalPage);
};

// Initial call to display the first page
showPage_siam_aisin(currentPage_siam_aisin);

// Previous button
document.getElementById('prev-btn_siam_aisin').addEventListener('click', function() {
    if (currentPage_siam_aisin > 1) {
        currentPage_siam_aisin--;
        showPage_siam_aisin(currentPage_siam_aisin);
    }
});
// Next button
document.getElementById('next-btn_siam_aisin').addEventListener('click', function() {
    if (currentPage_siam_aisin < Math.ceil(rows_siam_aisin.length / rowsPerPage_siam_aisin)) {
        currentPage_siam_aisin++;
        showPage_siam_aisin(currentPage_siam_aisin);
    }
});

// **************************** Siam Aisin ***************************************