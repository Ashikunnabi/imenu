/*
* =============================================================================
*                                   BANNER
* =============================================================================
**/

class Banner {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_home_page_a').click();
        $('#sidebar_option_banner').addClass('active');
    };

    /*
    * =========================================================================
    *                       Banner in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#bannerDataTable').DataTable({
            "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add banner',
                        id: 'addBannerButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = banner_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete banner',
                        id: 'deleteBannerButton',
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
                                    url: banner_api_url + data[0].hashed_id + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Banner has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
                        }
                                    }
                                });
                            }
                        })
                    }
                },
                {
                    extend: 'copy',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'pdf',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'excel',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'csv',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'print',
                    exportOptions: {orthogonal: 'export'}
                },
                // {
                //     extend: 'print',
                //     title: 'USERS',
                //     messageTop: '<h5 class="text-center">User List</h5>',
                //     messageBottom: null
                // }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': banner_api_url,
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
                {"title": "Page", "data": "human_readable_page"},
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
        $('#bannerDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#bannerDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.hashed_id;
        });
    };

    /*
    * =========================================================================
    *                       Banner add page dropdown setup
    * =========================================================================
    **/

    add_page_dropdown_value_set = (id='') => {
        // add banner form value setup
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
                let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
                        }
            }
        });
    };

    /*
    * =========================================================================
    *                       Banner add
    * =========================================================================
    **/

    add = () => {
        // set page dropdown
        this.add_page_dropdown_value_set();
        // add banner
        $(document).on('submit', '#banner_add', function (e) {
            e.preventDefault();
            const banner_add_form = $('#banner_add').parsley();
            let banner_add_form_data = new FormData($('#banner_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (banner_add_form.isValid()) {
                // is_active value set
                if (!banner_add_form_data.has('is_active')) banner_add_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: banner_api_url,
                    headers: {"X-CSRFToken": csrf_token},
                    type: "POST",
                    data: banner_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = banner_list_url;
                    },
                    error: function (response) {
                        let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
                        }
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                       Banner edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        let self = this;
        // edit banner form value setup
        $.ajax({
            url: banner_api_url + hashed_id,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editBannerCurrentImage').attr('href', `/media/${value}`) : "";
                        else if (key === 'page') self.add_page_dropdown_value_set(value);
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#banner_edit'), response);
            },
            error: function (response) {
                let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
                        }
            }
        });
    };

    /*
    * =========================================================================
    *                       Banner edit
    * =========================================================================
    **/

    edit = () => {
        // edit banner
        $(document).on('submit', '#banner_edit', function (e) {
            e.preventDefault();
            const banner_edit_form = $('#banner_edit').parsley();
            let banner_edit_form_data = new FormData($('#banner_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (banner_edit_form.isValid()) {
                // remove image attribute if no image uploaded
                if (banner_edit_form_data.has('image')) ($("input[name='image']").val() === '') ? banner_edit_form_data.delete('image') : '';
                if (!banner_edit_form_data.has('is_active')) banner_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: banner_api_url + hashed_id + '/',
                    headers: {"X-CSRFToken": csrf_token},
                    type: "PATCH",
                    data: banner_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        notify('Success', 'success', 2000);
                        setTimeout(() => {  window.location.reload(); }, 3000);
                    },
                    error: function (response) {
                        let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
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


new Banner().main();
