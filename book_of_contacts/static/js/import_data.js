/**
 * Created by vova on 28.05.17.
 */
var form_import = $("#form_for_import");
form_import.on("submit", function (e) {
    e.preventDefault();

    var data = new FormData($('#form_for_import').get(0));

       $.ajax({
           url: $(this).attr('action'),
           type: $(this).attr('method'),
           data: data,
           cache: false,
           processData: false,
           contentType: false,
           dataType: 'json',
           success: function (data) {
                alert('Your add: '+data.count+ 'row(s)');
               console.log(data.count);
           },
           error: function (error) {
                console.log(error);
           }
       });

       var re_init = $('#table_of_contacts').DataTable();  // reload dataTable
       re_init.ajax.reload();

       $('#btn-dismiss_import').click();  // close modal window "IMPORT"
});
