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

// **************************** FCC ***************************************

document.getElementById("Uploadbutton_fcc").onclick = function() {
    document.getElementById('fileInput_fcc').click();
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
var clearsoForm = document.getElementById('clearsoForm_fcc');
clearsoForm.addEventListener('submit', function(event) {
    event.preventDefault();

    var clearsoredirect = document.getElementById('clear_so_url_fcc').value;
    
    let clearsoMessage = document.getElementById('clearOrderMessage_fcc');
    fetch(clearsoredirect, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            clearsoMessage.classList.toggle("alert-success");
            clearsoMessage.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = clearsoredirect.substring(0, clearsoredirect.lastIndexOf('/'));
            }, 3000);
        } else {
            clearsoMessage.classList.toggle("alert-danger");
            clearsoMessage.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        clearsoMessage.classList.toggle("alert-danger");
        clearsoMessage.textContent = "Error: Could not clear sales order.";
        console.error(error);
    });
});

// Clear data function
var cleardataForm = document.getElementById('cleardataForm_fcc');
cleardataForm.addEventListener('submit', function(event) {
    event.preventDefault();

    var cleardataredirect = document.getElementById('clear_data_fcc').value;
    
    let clearDataMessage = document.getElementById('cleardataMessage_fcc');
    fetch(cleardataredirect, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            clearDataMessage.classList.remove("alert-danger");
            clearDataMessage.classList.add("alert-success");
            clearDataMessage.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = cleardataredirect.substring(0, cleardataredirect.lastIndexOf('/'));
            }, 3000);
        } else {
            clearDataMessage.classList.remove("alert-success");
            clearDataMessage.classList.add("alert-danger");
            clearDataMessage.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        clearDataMessage.classList.remove("alert-success");
        clearDataMessage.classList.add("alert-danger");
        clearDataMessage.textContent = "Error: Could not clear data.";
        console.error(error);
    });
});

// Sales order running function
var sorunningForm = document.getElementById('sorunningForm_fcc');
sorunningForm.addEventListener('submit', function(event) {
    event.preventDefault();

    var formSalesOrder = new FormData();
    var runningredirect = document.getElementById('sorunning_url_fcc').value;
    var elements = sorunningForm.elements;
    for(var i = 0; i < elements.length; i++) {
        var item = elements.item(i);
        formSalesOrder.append(item.name, item.value);
    }

    let salesorderMessage = document.getElementById('salesOrderMessage_fcc');
    fetch(runningredirect, {
        method: 'POST',
        body: formSalesOrder
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success) {
            salesorderMessage.classList.toggle("alert-success");
            salesorderMessage.textContent =  "Success: " + data.message;
            setTimeout (function () {
                window.location.href = runningredirect.substring(0, runningredirect.lastIndexOf('/'));
            }, 3000);
        } else {
            salesorderMessage.classList.toggle("alert-danger");
            salesorderMessage.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        salesorderMessage.classList.toggle("alert-danger");
        salesorderMessage.textContent = "Error: Could not running sales order.";
        console.error(error);
    });
});

document.querySelectorAll('button[type="submit"]').forEach(button => {
    button.addEventListener('click', function() {
        document.querySelectorAll('button[type="submit"]').forEach(btn => {
            btn.removeAttribute('name');
        });
        this.setAttribute('name',this.getAttribute('value'));
    });
});
//CIM Create function
var cimcreateForm = document.getElementById('cimcreateForm_fcc');
var buttonClicked = '';
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners here
    var exportButton = document.querySelector('input[name="export"]');
    var okButton = document.querySelector('button[name="ok"]');
    
    if (exportButton) {
        exportButton.addEventListener('click', function() {
            buttonClicked = 'export';
        });
    }
    
    if (okButton) {
        okButton.addEventListener('click', function() {
            buttonClicked = 'ok';
        });
    }
});
cimcreateForm.addEventListener('submit', function(event) {
    event.preventDefault();

    var formCreate = new FormData();
    var createurl = document.getElementById('cim_create_url_fcc').value;
    var filename = document.getElementById('outputfile_fcc').value;
    
    var elements = cimcreateForm.elements;

    for(var i=0; i < elements.length; i++) {
        var item = elements.item(i);
        formCreate.append(item.name, item.value);
    }

    let createMessage = document.getElementById('cim_create_message_fcc');

    if (buttonClicked === 'ok') {
        // Specific behavior for the "OK" button
        console.log("OK button pressed. Performing OK-specific action...");
        formCreate.delete("export")
        // You can modify createurl or other parameters as needed for the "OK" action
    } else if (buttonClicked === 'export') {
        // Specific behavior for the "export" button
        console.log("Export button pressed. Performing export-specific action...");
        formCreate.delete("ok")
    }

    fetch(createurl, {
        method: 'POST',
        body: formCreate
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
                createMessage.classList.remove("alert-danger");
                createMessage.classList.add("alert-success");
                createMessage.textContent = data.message;
                setTimeout (function () {
                    window.location.href = createurl.substring(0, createurl.lastIndexOf('/'));
                }, 3000);
            } else {
                createMessage.classList.remove("alert-success");
                createMessage.classList.add("alert-danger");
                createMessage.textContent = "Error: " + data.message;
            }
        } else if (data instanceof Blob) {
            // Try to export data
            const url = window.URL.createObjectURL(data);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename + '.cim';
            document.body.appendChild(a);
            a.click();
            a.remove();
        }
    })
    .catch(error => {
        // Handle any errors
        createMessage.classList.remove("alert-success");
        createMessage.classList.add("alert-danger");
        createMessage.textContent = "Error: Could not create CIM file.";
        console.error(error);
    });
});

// Transfer function
var transferForm = document.getElementById('uploadForm_fcc');
transferForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const submitTransfer = document.getElementById('transfer_submit_fcc');

    // Create a FormData object to hold the uploaded file
    var formData = new FormData();
    var fileInput = document.getElementById('fileInput_fcc');
    var redirecturl = document.getElementById('redirecturl_fcc').value;
    formData.append('file', fileInput.files[0]);
    var elements = transferForm.elements;
    // var obj ={};
    for(var i = 0; i < elements.length; i++){
        var item = elements.item(i);
        // obj[item.name] = item.value;
        formData.append(item.name, item.value);
    }

    let statusMessage = document.getElementById('uploadMessage_fcc');

    // Use fetch to send the form data to the server via POST
    fetch(redirecturl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        // Update the status message based on the server response
        if (data.success) {
            statusMessage.classList.remove("alert-danger");
            statusMessage.classList.add("alert-success");
            statusMessage.textContent = "File uploaded and data updated successfully!";
            submitTransfer.disabled = true;
            document.getElementById('transfer_submit_fcc').classList.toggle("disabled");
            setTimeout (function () {
                window.location.href = redirecturl.substring(0, redirecturl.lastIndexOf('/'));
            }, 3000);
        } else {
            statusMessage.classList.remove("alert-success");
            statusMessage.classList.add("alert-danger");
            statusMessage.textContent = "Error: " + data.message;
        }
    })
    .catch(error => {
        // Handle any errors
        statusMessage.classList.remove("alert-success");
        statusMessage.classList.add("alert-danger");
        statusMessage.textContent = "Error: Could not upload file.";
        console.error(error);
    });
});
function validatetransferForm() {
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
    console.log("true");
    return true;
};

// adjust for table style (8 records per page) 
const rows = document.querySelectorAll('.table-row');
const rowsPerPage = 7;
let currentPage = 1;

function showPage(page) {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    //Hide all rows
    rows.forEach(row => row.style.display = 'none');

    //Show thr rows only current page
    rows.forEach((row, index) => {
        if (index >= start && index < end) {
            row.style.display = 'table-row';
        }
    });

    var totalPage = Math.ceil(rows.length / rowsPerPage);
    if (totalPage === 0) {
        totalPage = 1;
    };

    document.getElementById('page-info_fcc').textContent = `Page ${page} of ${totalPage}`;
    document.getElementById('prev-btn_fcc').classList.toggle('disabled', page === 1);
    document.getElementById('next-btn_fcc').classList.toggle('disabled', page === totalPage);
};

// Initial call to display the first page
showPage(currentPage);

// Previous button
document.getElementById('prev-btn_fcc').addEventListener('click', function() {
    if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
    }
});
// Next button
document.getElementById('next-btn_fcc').addEventListener('click', function() {
    if (currentPage < Math.ceil(rows.length / rowsPerPage)) {
        currentPage++;
        showPage(currentPage);
    }
});

// **************************** FCC ***************************************