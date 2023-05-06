/*
* =============================================================================
*                                   BRAND
* =============================================================================
**/

class Group {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_inventory_a').click();
        $('#sidebar_option_inventory_group').addClass('active');
    };

    /*
    * =========================================================================
    *                       Group in Datatable
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
                        title: 'Add group',
                        id: 'addGroupButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = group_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete group',
                        id: 'deleteGroupButton',
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
                                $.ajax({
                                    url: api_urls["group_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Group has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        notify(response.responseText, 'error');
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
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': api_urls["group_list"],
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
                { "title": "Code", "data": "code" },
                { "title": "Name", "data": "name" },
                { "title": "Image", "data": "image" },
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
                    "targets": [3],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        if ([null, ""].indexOf(data)) return '';
                        return `<a href="/media/${data}" target="_blank">Image</a>`;
                    },
                },
                {
                    "targets": [4],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let active_html = `<i class="fa fa-solid fa-check color_green"></i>`
                        let inactive_html = `<i class="fa fa-times color_red"></i>`
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
    *                       GROUP SEARCH
    * =========================================================================
    **/
    group_search = (default_value = null) => {
        $("#parent_uuid").select2({
            // dropdownParent: $("#pos_section"),
            allowClear: true,
            placeholder: "Select group",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["group_list"],
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
            $('#parent_uuid').append(newOption).trigger('change');
            console.log(default_value)
        }
    }

    /*
    * =========================================================================
    *                       Group add
    * =========================================================================
    **/

    add = () => {
        // add group
        $(document).on('submit', '#group_add', function (e) {
            e.preventDefault();
            const group_add_form = $('#group_add').parsley();
            let group_add_form_data = new FormData($('#group_add')[0]);


            if (group_add_form.isValid()) {
                // is_active value set
                if (group_add_form_data.has('image')) ($("input[name='image']").val() === '') ? group_add_form_data.delete('image') : '';
                if (!group_add_form_data.has('is_active')) group_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["group_list"],
                    type: "POST",
                    data: group_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = group_list_url;
                    },
                    error: function (response) {
                        $.each(response.responseJSON.error, function (i, v) {
                            notify(`${i.toUpperCase()} - ${v}`, 'error')
                        })
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                       Group edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit group form value setup
        let self = this
        $.ajax({
            url: `${api_urls["group_list"]}${uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editGroupCurrentImage').attr('href', `/media/${value}`) : "";
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#group_edit'), response.data);

                // Select2 value set
                if (response.data.parent) {
                    let default_value = {
                        "id": response.data.parent.uuid,
                        "text": response.data.parent.name,
                    }
                    self.group_search(default_value = default_value);
                } else {
                    self.group_search();
                }
            },
            error: function (response) {
                $.each(response.responseJSON.error, function (i, v) {
                    notify(`${i.toUpperCase()} - ${v}`, 'error')
                })
            }
        });
    };

    /*
    * =========================================================================
    *                       Group edit
    * =========================================================================
    **/

    edit = () => {
        // edit group
        $(document).on('submit', '#group_edit', function (e) {
            e.preventDefault();
            const group_edit_form = $('#group_edit').parsley();
            let group_edit_form_data = new FormData($('#group_edit')[0]);

            if (group_edit_form.isValid()) {
                // remove image attribute if no image uploaded
                if (group_edit_form_data.has('image')) ($("input[name='image']").val() === '') ? group_edit_form_data.delete('image') : '';
                if (!group_edit_form_data.has('is_active')) group_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["group_list"] + uuid + '/',
                    type: "PATCH",
                    data: group_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        notify("Success", 'success')
                    },
                    error: function (response) {
                        $.each(response.responseJSON.error, function (i, v) {
                            notify(`${i.toUpperCase()} - ${v}`, 'error')
                        })
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
            this.group_search();
        };
        if (page_type === "edit") {
            this.edit_form_value_set();
            this.edit();
        }
    }
}


new Group().main();
