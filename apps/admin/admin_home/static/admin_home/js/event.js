/*
* =============================================================================
*                                   EVENT
* =============================================================================
**/

class Event {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_home_page_a').click();
        $('#sidebar_option_event').addClass('active');
    };

    /*
    * =========================================================================
    *                       Event in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#eventDataTable').DataTable({
            "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add event',
                        id: 'addEventButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = event_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete event',
                        id: 'deleteEventButton',
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
                                    url: event_api_url + data[0].hashed_id + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Event has been deleted.',
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
                'url': event_api_url,
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
                {"title": "Priority", "data": "priority"},
                {"title": "Title", "data": "title"},
                {"title": "Start Date", "data": "start_date"},
                {"title": "End Date", "data": "end_date"},
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
                    "targets": [6],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return `<a href="/media/${data}">Image</a>`;
                    },
                },
                {
                    "targets": [7],
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
        $('#eventDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#eventDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.hashed_id;
        });
    };

    /*
    * =========================================================================
    *                       Event add page dropdown setup
    * =========================================================================
    **/

    add_page_dropdown_value_set = (id='') => {
        // add event form value setup
        $.ajax({
            url: page_api_url,
            type: "get",
            success: function (response) {
                let options = '';
                $.each(response.data, function (key, value) {
                    let selected = (value.id === id) ? 'selected' : '';
                    options += `<option value="${value.hashed_id}" ${selected}>${value.title}</option>`
                });
                $('select[name=page]').html(options);
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
    *                       Event add
    * =========================================================================
    **/

    add = () => {
        // set page dropdown
        this.add_page_dropdown_value_set();
        // add event
        $(document).on('submit', '#event_add', function (e) {
            e.preventDefault();
            const event_add_form = $('#event_add').parsley();
            let event_add_form_data = new FormData($('#event_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
            

            if (event_add_form.isValid()) {
                // is_active value set
                if (!event_add_form_data.has('is_active')) event_add_form_data.append('is_active', 0);
                
                if (event_add_form_data.has('start_date')) {
                    event_add_form_data.set('start_date', `${$("input[name='start_date']").val()} 00:00:00`);
                }
                if (event_add_form_data.has('end_date')) {
                    event_add_form_data.set('end_date', `${$("input[name='end_date']").val()} 23:59:59`);
                }

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: event_api_url,
                    headers: {"X-CSRFToken": csrf_token},
                    type: "POST",
                    data: event_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = event_list_url;
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
    *                       Event edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        let self = this;
        // edit event form value setup
        $.ajax({
            url: event_api_url + hashed_id,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editEventCurrentImage').attr('href', `/media/${value}`) : "";
                        else if (key === 'page') self.add_page_dropdown_value_set(value);
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else if (key === 'start_date') $('[name=' + key + ']', form).val(value.split('T')[0]);
                        else if (key === 'end_date') $('[name=' + key + ']', form).val(value.split('T')[0]);
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#event_edit'), response);
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
    *                       Event edit
    * =========================================================================
    **/

    edit = () => {
        // edit event
        $(document).on('submit', '#event_edit', function (e) {
            e.preventDefault();
            const event_edit_form = $('#event_edit').parsley();
            let event_edit_form_data = new FormData($('#event_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (event_edit_form.isValid()) {
                // remove image attribute if no image uploaded
                if (event_edit_form_data.has('image')) ($("input[name='image']").val() === '') ? event_edit_form_data.delete('image') : '';
                if (!event_edit_form_data.has('is_active')) event_edit_form_data.append('is_active', 0);

                if (event_edit_form_data.has('start_date')) {
                    event_edit_form_data.set('start_date', `${$("input[name='start_date']").val()} 00:00:00`);
                }
                if (event_edit_form_data.has('end_date')) {
                    event_edit_form_data.set('end_date', `${$("input[name='end_date']").val()} 23:59:59`);
                }

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: event_api_url + hashed_id + '/',
                    headers: {"X-CSRFToken": csrf_token},
                    type: "PATCH",
                    data: event_edit_form_data,
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


new Event().main();
