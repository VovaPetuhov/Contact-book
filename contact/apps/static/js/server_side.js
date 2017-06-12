$(document).ready(function() {
    addContacts();
    init();
    updateContacts();
    delete_row();
    send_contacts();
    import_contacts()
    });

// Server-side processing for DataTable

function init() {
    var orderTable = $('#table_of_contacts').DataTable({
    "bServerSide": true,
    "sAjaxSource": 'list_of_contacts',
    "bProcessing": true,
    "bLengthChange": true,
    // "bSearching": true,
    "bFilter": true,
    'sDom': 'rtpli',
    "bSortable": false,  // change
    "autoWidth": true,
    "ordering": false,
    "bInfo": true,
    "lengthMenu": [[10, 25, 50, 100], [10, 25, 50, 100]],
    "iDisplayLength": 10,
    "aoColumnDefs": [
        {
        "mRender": function (data, type, row) {
            row.status_filter = '<a class="data_number" href="#">' + row[0] + '</a>';
            return row.status_filter;
        },
        "aTargets": [0]
        }
    ]

    });
}

var link_id = '';   // For definition of pressed link

// Show modal window ADD contact

function addContacts() {
    $("#my_modal_runner").click(function () {
//     e.preventDefault();
        var modal = $("#myModal");  //  Show modal window
        modal.modal({
            'keyboard': false,
            'backdrop': false,
            'show': true
        });
        modal.find('.add_input').val('');   //  Clear input fields
    });
}

// // Show modal window UPDATE or DELETE cotact

function updateContacts () {
    $("#table_of_contacts").on("click", ".data_number", function(event){
        link_id = event.target.text;
        // alert('You choose row number: ' + link_id);
        $('#myModalLabel_update').text('You choose row number: ' + link_id);
        var modal_update = $("#myModal_update");
        modal_update.modal({
            'keyboard': false,
            'backdrop': false,
            'show': true
        });

        var data = {};
        data.link_id = link_id;
        var csrf_token_2 = $('#form_update [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token_2;

        // Get data for input fields

        var url = form_2.attr("action");
        $.ajax({
            url: url+'get_value/',
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK_get");
                console.log(data.first_name_get);
                $('#number_first_name_update').val(data.first_name_get);
                $('#number_last_name_update').val(data.last_name_get);
                $('#number_country_update').val(data.country_get);
                $('#number_town_update').val(data.town_get);
                $('#number_phone_update').val(data.phone_nmb_get);
                $('#number_email_update').val(data.email_get);
            },
            error: function (data) {
                alert(data.description);
                console.log(data.description);
            }
        });
    });
    return false;
}

// After clicking on the "DELETE" button in the modal window "UPDATE",
// the selected contact from the database will be deleted

function delete_row() {
    $('#button_delete').click(function (e) {
        e.preventDefault();
        var data = {};
        data.link_id = link_id;
        var csrf_token_2 = $('#form_update [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token_2;

        var url = form_2.attr("action");
        $.ajax({
            url: url+'delete_row/',
            type: 'POST',
            data: data,
            cache: true,
            success: function () {
                console.log("OK_del");
                alert('You delete row number: ' + link_id);
            },
            error: function (data) {
                alert(data.description);
                console.log(data.description);
            }
        });

        var re_init = $('#table_of_contacts').DataTable();  // reload dataTable
        re_init.ajax.reload();

        $('#btn-dismiss_update').click();  // close modal window "ADD new contact"
    })
}

function send_contacts() {
    $('#button_for_api').click(function () {
        console.log('OK-BUTTON_SEND');
        var modal_api = $("#myModal_send");  //  Show modal window
        modal_api.modal({
            'keyboard': false,
            'backdrop': false,
            'show': true
        });
    });
}

function import_contacts() {
    $('#button_for_import').click(function () {
        console.log('OK-BUTTON_IMPORT');
        var modal_import = $("#myModal_import");  //  Show modal window
        modal_import.modal({
            'keyboard': false,
            'backdrop': false,
            'show': true
        });
    });
}
