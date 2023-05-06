/*
* =============================================================================
*                                   FLYER
* =============================================================================
**/

class Flyer {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_home_page_a').click();
        $('#sidebar_option_flyer').addClass('active');
    };

    /*
    * =========================================================================
    *                       Flyer in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#flyerDataTable').DataTable({
            "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add flyer',
                        id: 'addFlyerButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = flyer_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete flyer',
                        id: 'deleteFlyerButton',
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
                                    url: flyer_api_url + data[0].hashed_id + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Flyer has been deleted.',
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
                'url': flyer_api_url,
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
                {"title": "Title", "data": "title"},
                {"title": "Image", "data": "image"},
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
                    "targets": [1],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let icon = '';
                        if (row.is_promotional) icon+= ' <i class="fab fa-product-hunt text-info" title="Promotion"></i>'
                        if (row.show_at_home_page) icon+= ' <i class="fa fa-home text-primary" title="Showing at home page"></i>'
                        return `${data}${icon}`;
                    },
                },
                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return `<a href="/media/${data}">Image</a>`;
                    },
                },
                {
                    "targets": [3],
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
        $('#flyerDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#flyerDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.hashed_id;
        });
    };


    /*
    * =========================================================================
    *                       Flyer add
    * =========================================================================
    **/

    add = () => {
        // add flyer
        $(document).on('submit', '#flyer_add', function (e) {
            e.preventDefault();
            const flyer_add_form = $('#flyer_add').parsley();
            let flyer_add_form_data = new FormData($('#flyer_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (flyer_add_form.isValid()) {
                // is_active value set
                if (!flyer_add_form_data.has('show_at_home_page')) flyer_add_form_data.append('show_at_home_page', 0);
                if (!flyer_add_form_data.has('is_promotional')) flyer_add_form_data.append('is_promotional', 0);
                if (!flyer_add_form_data.has('is_active')) flyer_add_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: flyer_api_url,
                    headers: {"X-CSRFToken": csrf_token},
                    type: "POST",
                    data: flyer_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = flyer_list_url;
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
    *                       Flyer edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        let self = this;
        // edit flyer form value setup
        $.ajax({
            url: flyer_api_url + hashed_id,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editFlyerCurrentImage').attr('href', `/media/${value}`) : "";
                        else if (key === 'image1') (value != null) ? $('#editFlyerCurrentImage1').attr('href', `/media/${value}`) : "";
                        else if (key === 'image2') (value != null) ? $('#editFlyerCurrentImage2').attr('href', `/media/${value}`) : "";
                        else if (key === 'image3') (value != null) ? $('#editFlyerCurrentImage3').attr('href', `/media/${value}`) : "";
                        else if (key === 'show_at_home_page') (value === true) ? $('input[name=show_at_home_page]').click() : "";
                        else if (key === 'is_promotional') (value === true) ? $('input[name=is_promotional]').click() : "";
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#flyer_edit'), response);
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
    *                       Flyer edit
    * =========================================================================
    **/

    edit = () => {
        // edit flyer
        $(document).on('submit', '#flyer_edit', function (e) {
            e.preventDefault();
            const flyer_edit_form = $('#flyer_edit').parsley();
            let flyer_edit_form_data = new FormData($('#flyer_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (flyer_edit_form.isValid()) {
                // remove image attribute if no image uploaded
                if (flyer_edit_form_data.has('image')) ($("input[name='image']").val() === '') ? flyer_edit_form_data.delete('image') : '';
                if (flyer_edit_form_data.has('image1')) ($("input[name='image1']").val() === '') ? flyer_edit_form_data.delete('image1') : '';
                if (flyer_edit_form_data.has('image2')) ($("input[name='image2']").val() === '') ? flyer_edit_form_data.delete('image2') : '';
                if (flyer_edit_form_data.has('image3')) ($("input[name='image3']").val() === '') ? flyer_edit_form_data.delete('image3') : '';
                if (!flyer_edit_form_data.has('show_at_home_page')) flyer_edit_form_data.append('show_at_home_page', 0);
                if (!flyer_edit_form_data.has('is_promotional')) flyer_edit_form_data.append('is_promotional', 0);
                if (!flyer_edit_form_data.has('is_active')) flyer_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: flyer_api_url + hashed_id + '/',
                    headers: {"X-CSRFToken": csrf_token},
                    type: "PATCH",
                    data: flyer_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        notify('Success', 'success', 2000);
                        setTimeout(() => {  window.location.reload(); }, 3000);
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


new Flyer().main();
