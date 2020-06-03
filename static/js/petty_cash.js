// Show datepicker when user clicks "Date" input field
$(function() {
    $( "#datepicker" ).datepicker();
  });


d3.selectAll('#submit-btn').on('click', buildTable);

function buildTable() {
    var dateInput = d3.select('#datepicker').property('value');
    var receiptInput = d3.select('#receiptNumber').property('value');
    var description = d3.select('#description').property('value');
    var depAmount = d3.select('#depAmount').property('value');
    var withAmount = d3.select('#withAmount').property('value');
    var receivedBy = d3.select('#receivedBy').property('value');
    var approvedBy = d3.select('#approvedBy').property('value');
    var comments = d3.select('#comments').property('value');

    var tableArray = []
    tableArray.push(dateInput, receiptInput, description, depAmount, withAmount, receivedBy, approvedBy, comments)
    console.log(tableArray);

    var row = d3.select('tbody').append('tr');
    
    tableArray.forEach(function(x) {
  
        var cell = row.append('td');
        cell.text(x);
    });

    localStorage.setItem('show', 'true');

    d3.selectAll("tr").on("click", function() {
      console.log('test');
    });

};

