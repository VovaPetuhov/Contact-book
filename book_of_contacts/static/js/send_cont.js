var form_3 = $("#form_for_api");
form_3.on('submit', function (e) {
    e.preventDefault();

    var data = {};
        data.status_user = true;

        var csrf_token_3 = $('#form_for_api [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token_3;

        // Send data to back-end

        var url = form_3.attr("action");
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK_send");
                if (data.status_user_POST == false) {
                    alert('Enter the API key on the page "Settings"');
                }
            },
            error: function () {
                console.log("error_send");
            }
        });
        $('#btn-dismiss_send').click();
});