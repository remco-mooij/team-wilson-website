$(document).ready(function(){

    $('#submit-btn').click(function() {

        var dateInput = $('#datepicker').val();
        var receiptInput = $('#receiptNumber').val();
        var description = $('#description').val();
        var depAmount = $('#depAmount').val();
        var withAmount = $('#withAmount').val();
        var receivedBy = $('#receivedBy').val();
        var approvedBy = $('#approvedBy').val();
        var comments = $('#comments').val();

        console.log(dateInput);

        var tableArray = []
        tableArray.push(dateInput, receiptInput, description, depAmount, withAmount, receivedBy, approvedBy, comments)
        console.log(tableArray);


        var tbody = $('#tbody');
        var row = $('<tr>');

        tableArray.forEach(function(x) {

            var cell = ('<td>' + x + '</td>');
            row.append(cell);
            
        });
            
        tbody.append(row);

    });

});
