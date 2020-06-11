


$(document).ready(function() {

    $(function() {
        $(".datepicker").datepicker();
    });

    $('#enterTrans').on('submit', function(event) {
        
        $.ajax({
            data: {
                expDate : $('#datepicker').val(),
                expReceipt: $('#receiptNumber').val(),
                expDescr: $('#description').val(),
                expAmountDep: $('#depAmount').val(),
                expAmountWith: $('#withAmount').val(),
                expReceived: $('#receivedBy').val(),
                expApproved: $('#approvedBy').val(),
                expComments: $('#comments').val()
            },
            type : 'POST',
            url : '/submit'
        })
        .done(function(data) {

            if (data.error) {
                $('#errorAlert').text(data.error).show();
            }
            else {
                var dateInput = data.message;
                var receiptInput = data.receipt;
                var description = data.descr;
                var depAmount = data.amountDep;
                var withAmount = data.amountWith;
                var receivedBy = data.received;
                var approvedBy = data.approved;
                var comments = data.comments;

                var tableArray = []
                tableArray.push(dateInput, receiptInput, description, depAmount, withAmount, receivedBy, approvedBy, comments);
                console.log(tableArray);

                var tbody = $('#tbody');
                var row = $('<tr>');

                tableArray.forEach(function(x) {
                    var cell = ('<td>' + x + '</td>');
                    row.append(cell);
                });
                    
                tbody.append(row);

                $('#successAlert').text('test').show();
            };
        });

        event.preventDefault();
    });

    $('#filterTrans').on('submit', function(event) {
        
        $.ajax({
            data: {
                fromDate : $('#fromDate').val(),
                toDate: $('#toDate').val(),
            },
            type : 'POST',
            url : '/filter'
        })
        .done(function(data) {

            if (data.error) {
                $('#errorAlert').text(data.error).show();
            }
            else {
                $('#successAlert').text(data.result).show();
                var filteredData = data.result;
                console.log(filteredData);
                var tableArray = []

                // var dateInput = $('#datepicker').val();
                // var receiptInput = $('#receiptNumber').val();
                // var description = $('#description').val();
                // var depAmount = $('#depAmount').val();
                // var withAmount = $('#withAmount').val();
                // var receivedBy = $('#receivedBy').val();
                // var approvedBy = $('#approvedBy').val();
                // var comments = $('#comments').val();

                // var tableArray = []
                // tableArray.push(dateInput, receiptInput, description, depAmount, withAmount, receivedBy, approvedBy, comments);
                // console.log(tableArray);

                // var tbody = $('#tbody');
                // var row = $('<tr>');

                // tableArray.forEach(function(x) {
                //     var cell = ('<td>' + x + '</td>');
                //     row.append(cell);
                // });
                    
                // tbody.append(row);

                // $('#successAlert').text('test').show();
            };
        });

        event.preventDefault();
    });



});