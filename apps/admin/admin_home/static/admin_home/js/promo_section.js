/*
* =============================================================================
*                                   PROMO SECTION
* =============================================================================
**/

class PromoSection {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_home_page_a').click();
        $('#sidebar_option_promo_section').addClass('active');
    };

    /*
    * =========================================================================
    *                       Promo Section in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#promoSectionDataTable').DataTable({
            "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add promo',
                        id: 'addPromoSectionButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = promo_section_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete promo',
                        id: 'deletePromoSectionButton',
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
                                    url: promo_section_api_url + data[0].hashed_id + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Promo has been deleted.',
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
                'url': promo_section_api_url,
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
                {"title": "Promo", "data": "promo"},
                {"title": "Redirect Url", "data": "redirect_url"},
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
                    "targets": [4],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return `<a href="/media/${data}">Image</a>`;
                    },
                },
                {
                    "targets": [5],
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
        $('#promoSectionDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#promoSectionDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.hashed_id;
        });
    };

    /*
    * =========================================================================
    *                       Promo Section add
    * =========================================================================
    **/

    add = () => {
        // add promo section
        $(document).on('submit', '#promo_section_add', function (e) {
            e.preventDefault();
            const promo_section_add_form = $('#promo_section_add').parsley();
            let promo_section_add_form_data = new FormData($('#promo_section_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (promo_section_add_form.isValid()) {
                // is_active value set
                if (!promo_section_add_form_data.has('is_active')) promo_section_add_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: promo_section_api_url,
                    headers: {"X-CSRFToken": csrf_token},
                    type: "POST",
                    data: promo_section_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = promo_section_list_url;
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
    *                       Promo Section edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit promo section form value setup
        $.ajax({
            url: promo_section_api_url + hashed_id,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editPromoSectionCurrentImage').attr('href', `/media/${value}`) : "";
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#promo_section_edit'), response);
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
    *                       Promo Section edit
    * =========================================================================
    **/

    edit = () => {
        // edit promo section
        $(document).on('submit', '#promo_section_edit', function (e) {
            e.preventDefault();
            const promo_section_edit_form = $('#promo_section_edit').parsley();
            let promo_section_edit_form_data = new FormData($('#promo_section_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (promo_section_edit_form.isValid()) {
                // remove image attribute if no image uploaded
                if (promo_section_edit_form_data.has('image')) ($("input[name='image']").val() === '') ? promo_section_edit_form_data.delete('image') : '';
                if (!promo_section_edit_form_data.has('is_active')) promo_section_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: promo_section_api_url + hashed_id + '/',
                    headers: {"X-CSRFToken": csrf_token},
                    type: "PATCH",
                    data: promo_section_edit_form_data,
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


new PromoSection().main();
