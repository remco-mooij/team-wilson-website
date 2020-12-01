
$(document).ready(function() {

    $(function() {
        $(".datepicker").datepicker();
    });

    var clicked = false;


//     $('#enterTrans').on('submit', function(event) {
//         if (clicked === true) {
//             $('#tbody').find('tr').remove();
//             clicked = false;
//         };
        
//         $.ajax({
//             data: {
//                 expDate: $('#datepicker').val(),
//                 expReceipt: $('#receiptNumber').val(),
//                 expDescr: $('#description').val(),
//                 expAmountDep: $('#depAmount').val(),
//                 expAmountWith: $('#withAmount').val(),
//                 expReceived: $('#receivedBy').val(),
//                 expApproved: $('#approvedBy').val(),
//                 expComments: $('#comments').val()
//             },
//             type : 'POST',
//             url : '/submit'
//         })
//         .done(function(data) {

//             if (data.error) {
//                 $('#errorAlert').text(data.error).show();
//             }
//             else {
//                 var dateInput = data.transDate;
//                 var receiptInput = data.receipt;
//                 var description = data.descr;
//                 var depAmount = data.amountDep;
//                 var withAmount = data.amountWith;
//                 var receivedBy = data.received;
//                 var approvedBy = data.approved;
//                 var comments = data.comments;
               

//                 var tableArray = []
//                 tableArray.push(dateInput, receiptInput, description, depAmount, withAmount, receivedBy, approvedBy, comments);

//                 var tbody = $('#tbody');
//                 var row = $('<tr>');

//                 tableArray.forEach(function(x) {
//                     var cell = ('<td>' + x + '</td>');
//                     row.append(cell);
//                 });
                    
//                 tbody.append(row);

//                 $('#successAlert').text(data.date).show();
//             };
//         });

//         event.preventDefault();
//     });



});