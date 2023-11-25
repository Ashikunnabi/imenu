/*
* =============================================================================
*                                Attribute
* =============================================================================
**/

class Attribute {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_inventory_a').click();
        $('#sidebar_option_inventory_attribute').addClass('active');
    };

    /*
    * =========================================================================
    *                        Attribute  in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add Attribute',
                        id: 'addAttributeButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = attribute_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete Attribute',
                        id: 'deleteAttributeButton',
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
                                    url: api_urls["attribute_list"] + data[0].uuid + '/',
                                    headers: { "X-CSRFToken": csrf_token },
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Attribute  has been deleted.',
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
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': api_urls["attribute_list"],
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function (row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Name", "data": "name" },
                { "title": "Status", "data": "is_active" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let active_html = `<i class="fa fa-solid fa-check color_green"></i>`
                        let inactive_html = `<i class="fa fa-times color_red"></i>`
                        if (type === "export") {
                            if (data) return "Active"
                            return "Inactive"
                        }
                        if (data) return active_html
                        return inactive_html
                    },
                },
            ],
        });

        // Single click row select the row and mark a different color
        $('#dataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       ATTRIBUTE GROUP SEARCH
    * =========================================================================
    **/
    attribute_group_search = (default_value = null) => {
        $("#attribute_group_uuid").select2({
            // dropdownParent: $("#pos_section"),
            allowClear: true,
            placeholder: "Select attribute group",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["attribute_group_list"],
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.uuid,
                            text: `${v.name}`,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });

        if (default_value) {
            let newOption = new Option(default_value.text, default_value.id, true, true);
            $('#attribute_group_uuid').append(newOption).trigger('change');
            console.log(default_value)
        }
    }

    /*
    * =========================================================================
    *                        Attribute  add
    * =========================================================================
    **/

    add = () => {
        $(document).on('submit', '#attribute_add', function (e) {
            e.preventDefault();
            const attribute_add_form = $('#attribute_add').parsley();
            let attribute_add_form_data = new FormData($('#attribute_add')[0]);

            if (attribute_add_form.isValid()) {
                // is_active value set
                if (!attribute_add_form_data.has('is_active')) attribute_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["attribute_list"],
                    type: "POST",
                    contentType: false,
                    processData: false,
                    data: attribute_add_form_data,
                    success: function (response) {
                        window.location.href = attribute_list_url;
                    },
                    error: function (response) {
                        notify(`${response.responseJSON.message}`, 'error')
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                        Attribute  edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        let self = this;
        $.ajax({
            url: `${api_urls["attribute_list"]}${uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#attribute_edit'), response.data);

                // Select2 value set
                if (response.data.attribute_group) {
                    let default_value = {
                        "id": response.data.attribute_group.uuid,
                        "text": response.data.attribute_group.name,
                    }
                    self.attribute_group_search(default_value = default_value);
                } else {
                    self.attribute_group_search();
                }

            },
            error: function (response) {
                notify(response.responseJSON.details, 'error')
            }
        });
    };

    /*
    * =========================================================================
    *                        Attribute  edit
    * =========================================================================
    **/

    edit = () => {
        $(document).on('submit', '#attribute_edit', function (e) {
            e.preventDefault();
            const attribute_edit_form = $('#attribute_edit').parsley();
            let attribute_edit_form_data = new FormData($('#attribute_edit')[0]);

            if (attribute_edit_form.isValid()) {
                if (!attribute_edit_form_data.has('is_active')) attribute_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["attribute_list"] + uuid + '/',
                    type: "PATCH",
                    data: attribute_edit_form_data,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        notify("Success", 'success')
                    },
                    error: function (response) {
                        notify(response.responseJSON.details, 'error')
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
        if (page_type === "list") this.list();
        if (page_type === "add") {
            this.add();
            this.attribute_group_search();
        };
        if (page_type === "edit") {
            this.edit_form_value_set();
            this.edit();
        }
    }
}


new Attribute().main();
