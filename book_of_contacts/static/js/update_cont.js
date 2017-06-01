var form_2 = $("#form_update");
form_2.on('submit', function (e) {
    e.preventDefault();

    console.log('second');

    var first_name = $('#number_first_name_update').val();
    var last_name = $('#number_last_name_update').val();
    var country = $('#number_country_update').val();
    var town = $('#number_town_update').val();
    var phone_nmb = $('#number_phone_update').val();
    var email = $('#number_email_update').val();

    var data = {};
        data.link_id = link_id;
        data.first_name = first_name;
        data.last_name = last_name;
        data.country = country;
        data.town = town;
        data.phone_nmb = phone_nmb;
        data.email = email;
        console.log(data);

        var csrf_token_2 = $('#form_update [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token_2;

        // Send data to back-end

        var url = form_2.attr("action");
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK_update");

            },
            error: function () {
                console.log("error_update");
            }
        });

        var re_init = $('#table_of_contacts').DataTable();  // reload dataTable
        re_init.ajax.reload();

        $('#btn-dismiss_update').click(); // close modal window
});
