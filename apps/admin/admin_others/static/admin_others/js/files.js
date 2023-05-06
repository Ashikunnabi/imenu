/*
* =============================================================================
*                                   PRODUCT IMAGE
* =============================================================================
**/

class SalesReps {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_others_a').click();
        $('#sidebar_option_others_product_image').addClass('active');
    };

    /*
    * =========================================================================
    *                       PRODUCT IMAGE in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#filesDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add New Files',
                        id: 'addFilesButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        (async () => {
                            const { value: file } = await Swal.fire({
                              title: 'Upload files',
                              html:
                                `<div style="text-align:left">
                                    <input type="file" multiple="multiple" id="swal2-file" class="swal2-file" placeholder="" style="display: flex;">
                                    <hr>
                                    <select id="swal-user" style="width:100%"></select><br><br>
                                    <input type="checkbox" id="swal-is_encrypted"> <label for="swal-is_encrypted">Encrypt</label>
                                </div>`,
                              showCancelButton: true,
                              confirmButtonColor: '#3085d6',
                              cancelButtonColor: '#d33',
                              confirmButtonText: 'Upload'
                            });

                            if (file) {
                                let formData = new FormData();
                                $.each($("#swal2-file")[0].files, function(i, e) {
                                    formData.append('files', e);
                                })
                                
                                formData.append('user', $("#swal-user").val());
                                formData.append('type', 'others');
                                formData.append('is_encrypted', $("#swal-is_encrypted").is(":checked"));

                                // do ajax request to upload file
                                $.blockUI();
                                $.ajax({
                                    url: files_api_url,
                                    type: "POST",
                                    data : formData,
                                    processData: false,  // tell jQuery not to process the data
                                    contentType: false,  // tell jQuery not to set contentType
                                    success: function (resp) {
                                        Swal.fire(
                                            'Uploaded!',
                                            'File(s) uploaded successfully.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        $.unblockUI();
                                        notify(response.responseJSON.details, 'error')
                                    },
                                    complete: function (response) {
                                        $.unblockUI()
                                    }
                                });
                            }
                        })()
                        
                        $("#swal-user").select2({
                            placeholder: "Select a user",
                            allowClear: true,
                            minimumInputLength: 3,
                            dropdownParent: $('#swal2-content'),
                            ajax: {
                                url: '/api/v1/dealer/?key=name',
                                dataType: 'json',
                                processResults: function (data) {
                                    // Transforms the top-level key of the response object from 'items' to 'results'
                                    let results = []
                                    $.each(data, function(i, v) {
                                        results.push({
                                            id: v.id,
                                            text: v.name,
                                            other: v
                                        })
                                    })
                                    return {
                                        results: results
                                    };
                                }
                            }
                        })  
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete Product Image',
                        id: 'deleteFilesButton',
                        class: 'btn btn-danger'
                    },
                    action: function (e, dt, node, config) {
                        let data = dt.rows(".selected").data();
                        // no table row selected
                        if (data[0] === undefined) {
                            notify('Please select an item', 'error');
                            return;
                        }
                        // table row selected so do further actions
                        Swal.fire({
                            title: 'Are you sure?',
                            text: "You won't be able to revert this!",
                            icon: 'warning',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes, delete it!'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
                                // do ajax request to delete
                                $.ajax({
                                    url: files_api_url + data[0].uuid + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Product image has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        if (response.status === 422) {
                                            let errors = '';
                                            $.map(response.responseJSON.details, function (v, i) {
                                                $.each(v, function (j, k) {
                                                    errors += `<li>${i}: ${k}</l1>`;
                                                })
                                            });
                                            let final_error = `<ul>${errors}</ul>`;

                                            $('.failed')
                                                .html(final_error)
                                                .css('display', 'block')
                                        }
                                        notify(response.responseJSON.detail, 'error');
                                    }
                                });
                            }
                        })
                    }
                },
                'copy',
                'excel',
                'pdf',
                'csv',
                'print',
                // {
                //     extend: 'print',
                //     title: 'USERS',
                //     messageTop: '<h5 class="text-center">User List</h5>',
                //     messageBottom: null
                // }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': files_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "URL", "data": "file"},
                {"title": "User", "data": "user_full_name"},
                {"title": "Encrypted", "data": "is_encrypted"},
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    targets: 1,
                    width: '20%',
                    render: function (data, type, row, meta) {
                        if (data) {
                            let url = `${window.location.origin}/media/${data}`
                            let html = `${url} &nbsp;&nbsp; <a href="${url}" target="_blank"><i class="fa fa-link" aria-hidden="true"></i></a>`
                            return html;
                        }
                    }
                },
                {
                    "targets": [3],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        if (data) {
                            let html = `<i class="fa fa-check" style="color:green;"></i> &nbsp;&nbsp; | &nbsp;&nbsp; 
                            <i class="fa fa-unlock-alt" aria-hidden="true" onclick="Decrypt('${row["file"]}')" title="Decrypt this"></i>`
                            return html;
                        }
                        return `<i class="fa fa-times" style="color:red;"></i> &nbsp;&nbsp; | &nbsp;&nbsp; 
                        <i class="fa fa-lock" aria-hidden="true" onclick="Encrypt('${row["file"]}')" title="Encrypt this"></i>`
                    },
                },
            ],
        });

        // Single click row select the row and mark a different color
        $('#filesDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });
    };

    /*
   * =========================================================================
   *                       Encrypt file
   * =========================================================================
   **/

    encrypt_file = (file_path) => {

        $.ajax({
            url: files_api_url + "encrypt/",
            type: "POST",
            data: JSON.stringify({"file_path": file_path}),
            cache: false,
            contentType: "application/json",
            processData: false,
            success: function (resp) {
                window.location.reload();
            },
            error: function (response) {
                if (response.status === 422) {
                    let errors = '';
                    $.map(response.responseJSON.details, function (v, i) {
                        $.each(v, function (j, k) {
                            errors += `<li>${i}: ${k}</l1>`;
                        })
                    });
                    let final_error = `<ul>${errors}</ul>`;

                    $('.failed')
                        .html(final_error)
                        .css('display', 'block')
                }
            }
        });
    }

    /*
   * =========================================================================
   *                       Decrypt file
   * =========================================================================
   **/

    decrypt_file = (file_path) => {

        $.ajax({
            url: files_api_url + "decrypt/",
            type: "POST",
            data: JSON.stringify({"file_path": file_path}),
            cache: false,
            contentType: "application/json",
            processData: false,
            success: function (resp) {
                window.location.reload();
            },
            error: function (response) {
                if (response.status === 422) {
                    let errors = '';
                    $.map(response.responseJSON.details, function (v, i) {
                        $.each(v, function (j, k) {
                            errors += `<li>${i}: ${k}</l1>`;
                        })
                    });
                    let final_error = `<ul>${errors}</ul>`;

                    $('.failed')
                        .html(final_error)
                        .css('display', 'block')
                }
            }
        });
    }

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.select_sidebar_option();
        this.list();
    }
}

function Encrypt(file_path) {
    new SalesReps().encrypt_file(file_path)
}

function Decrypt(file_path) {
    new SalesReps().decrypt_file(file_path)
}


new SalesReps().main();
