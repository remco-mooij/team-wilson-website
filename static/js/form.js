$(document).ready(function() {

    $('form').on('submit', function(event) {
        
        $.ajax({
            data : {
                expDate: $('#datepicker').val(),
                expReceipt: $('#receiptNumber').val(),
                expDescr: $('#description').val(),
                expAmountDep: $('#depAmount').val(),
                expAmountWith: $('#withAmount').val(),
                expReceived: $('receivedBy').val(),
                

            },
            type : 'POST',
            url : '/submit'
        })
        .done(function(data) {

            if (data.error) {
                $('#errorAlert').text(data.error).show();
            }
            else {
     
                $('#successAlert').text(data.message).show();
            }
            
        });



        event.preventDefault();
    });

});