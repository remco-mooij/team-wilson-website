// from data.js
var tableData = data;

// YOUR CODE HERE!
table = {}

var button = d3.select("#filter-btn");

button.on("click", function() {
    d3.selectAll("tbody>tr").remove();

    var nameInput = d3.select("#name").property("value");
    var idInput = d3.select("#customer-id").property("value");
    var soInput = d3.select("#sales-order").property("value");

    console.log(nameInput);

    if (nameInput !== "") {
        var regexpName = new RegExp(nameInput, 'i');

        var filteredName = tableData.filter(transaction =>
        regexpName.test(transaction.customerName));

        filteredName.forEach((transaction) => {
            var row = d3.select("tbody").append("tr");
            Object.entries(transaction).forEach(([key, value]) => {
                var cell = row.append("td");
                cell.text(value);
            });
        });

        document.getElementById('name').value = "";
    }

    else if (idInput !== "") {
        var regexpId = new RegExp(idInput, 'i');

        var filteredId = tableData.filter(transaction =>
            regexpId.test(transaction.customerCode));

        filteredId.forEach((transaction) => {
            var row = d3.select("tbody").append("tr");
            Object.entries(transaction).forEach(([key, value]) => {
                var cell = row.append("td");
                cell.text(value);
                });
            });

        document.getElementById('customer-id').value = "";
    }

    else if (soInput !== "") {
        var regexpSo = new RegExp(soInput, 'i');
        
        var filteredSo = tableData.filter(transaction =>
            regexpSo.test(transaction.salesOrder));

        filteredSo.forEach((transaction) => {
            var row = d3.select("tbody").append("tr");
            Object.entries(transaction).forEach(([key, value]) => {
                var cell = row.append("td");
                cell.text(value);
                });
            });

        document.getElementById('sales-order').value = "";
    };

});
 
        






