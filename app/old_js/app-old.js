// from data.js
var tableData = data;

// YOUR CODE HERE!
table = {}

var button = d3.select("#filter-btn");





button.on("click", function() {
    d3.selectAll("tbody>tr").remove();

    var nameInput = d3.select("#name").property("value");
    var idInput = d3.select("#customer-id").property("value");

    
    var regexpName = new RegExp(nameInput, 'i');
    var regexpId = new RegExp(idInput, 'i');
    
    console.log(regexpId);

    var filteredName = tableData.filter(transaction =>
        regexpName.test(transaction.customerName));

    var filteredId = tableData.filter(transaction =>
        regexpId.test(transaction.customerCode));

    // var filteredName = tableData.filter(transaction => transaction.customerName.includes(nameInput));
    // var filteredId = tableData.filter(transaction => transaction.customerCode === idInput);
 
        
    if (regexpName !== "/(?:)/i") {
    filteredName.forEach((transaction) => {
        var row = d3.select("tbody").append("tr");
        Object.entries(transaction).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });

    if (regexpId !== "/(?:)/i") {
    filteredId.forEach((transaction) => {
        var row = d3.select("tbody").append("tr");
        Object.entries(transaction).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });
};

});

