/*
* =============================================================================
*                                   SALES REPS
* =============================================================================
**/

class SalesReps {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_user_management_a').click();
        $('#sidebar_option_user_management_sales_reps').addClass('active');
    };

    /*
    * =========================================================================
    *                       Sales Reps in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#salesRepsDataTable').DataTable({
            // "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add Sales Reps',
                        id: 'addSalesRepsButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = sales_reps_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete Sales Reps',
                        id: 'deleteSalesRepsButton',
                        class: 'btn btn-danger'
                    },
                    action: function (e, dt, node, config) {
                        let data = dt.rows(".selected").data();
                        // no table row selected
                        if (data[0] === undefined) {
                            notify('Please select an reps', 'error');
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
                                    url: sales_reps_api_url + data[0].uuid + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Sales Reps has been deleted.',
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
                'url': sales_reps_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function(row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "Image", "data": "image"},
                {"title": "Title", "data": "title"},
                {"title": "Name", "data": "name"},
                {"title": "Email", "data": "email"},
                {"title": "Phone", "data": "phone"},
                {"title": "Status", "data": "is_active"},
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
                    render: function (data, type, row, meta) {
                        if (data) {
                            return `<a href="/media/${data}" target="_blank">Image</a>`;
                        }
                    }
                },
                {
                    "targets": [6],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        if (data) return 'Active';
                        return 'Inactive'
                    },
                },
            ],
        });

        // Single click row select the row and mark a different color
        $('#salesRepsDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#salesRepsDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       Sales Reps add
    * =========================================================================
    **/

    add = () => {
        // add Sales Reps 
        $(document).on('submit', '#sales_reps_add', function (e) {
            e.preventDefault();
            const sales_reps_add_form = $('#sales_reps_add').parsley();
            let sales_reps_add_form_data = new FormData($('#sales_reps_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (sales_reps_add_form.isValid()) {
                // make form attributes request friendly
                // if (!sales_reps_add_form_data.has('is_active')) sales_reps_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: sales_reps_api_url,
                    headers: {"X-CSRFToken": csrf_token},
                    type: "POST",
                    data: sales_reps_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = sales_reps_list_url;
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
        });
    };

    /*
    * =========================================================================
    *                       Sales Reps  edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit Sales Reps  form value setup
        $.ajax({
            url: sales_reps_api_url + uuid,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editSalesRepsImage').attr('href', `/media/${value}`) : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#sales_reps_edit'), response);
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
    };

    /*
    * =========================================================================
    *                       Sales Reps  edit
    * =========================================================================
    **/

    edit = () => {
        // edit Sales Reps
        $(document).on('submit', '#sales_reps_edit', function (e) {
            e.preventDefault();
            const sales_reps_form = $('#sales_reps_edit').parsley();
            let sales_reps_form_data = new FormData($('#sales_reps_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (sales_reps_form.isValid()) {
                // make form attributes request friendly
                // if (!sales_reps_form_data.has('is_active')) sales_reps_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: sales_reps_api_url + uuid + '/',
                    headers: {"X-CSRFToken": csrf_token},
                    type: "PATCH",
                    data: sales_reps_form_data,
                    cache: false,
                    contentType: false,
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
                        } else {
                            notify(response.responseJSON.detail, 'error');
                        }
                    }
                });
            }
        });
    };

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.select_sidebar_option();
        this.list();
        this.add();
        this.edit_form_value_set();
        this.edit();
    }
}


new SalesReps().main();
