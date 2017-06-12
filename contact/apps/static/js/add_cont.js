var form = $("#form_add");
form.on("submit", function (e) {
    e.preventDefault();

    var btn = $(".btn-add");
    var btn_id = btn.data("id");

    var first_name = $('#number_first_name').val();
    var last_name = $('#number_last_name').val();
    var country = $('#number_country').val();
    var town = $('#number_town').val();
    var phone_nmb = $('#number_phone').val();
    var email = $('#number_email').val();

    var data = {};
        data.id = btn_id;
        data.first_name = first_name;
        data.last_name = last_name;
        data.country = country;
        data.town = town;
        data.phone_nmb = phone_nmb;
        data.email = email;
        console.log(data);

        var csrf_token = $('#form_add [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        // Send data to back-end

        var url = form.attr("action");
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK_add");
                alert(data.description);
            },
            error: function () {
                console.log("error_add");
                alert(data.description);
            }
        });

        var re_init = $('#table_of_contacts').DataTable();  // reload dataTable
        re_init.ajax.reload();

        $('#btn-add_dismiss').click();  // close modal window "ADD new contact"
    });

