/*
* =============================================================================
*                                   MENU TYPE
* =============================================================================
**/

class MenuType {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_table_a').click();
        $('#sidebar_option_table_type').addClass('active');
    };

    /*
    * =========================================================================
    *                       Product in Datatable
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
                        title: 'Add table type',
                        id: 'addMenuTypeButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = table_type_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete table type',
                        id: 'deleteMenuTypeButton',
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
                                    url: api_urls["table_type_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Table type has been deleted.',
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
                'url': api_urls["table_type_list"],
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
                { "title": "Is Active", "data": "is_active" },
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
            // self.edit_form_value_set(table, data.uuid);
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       Menu add
    * =========================================================================
    **/

    add = () => {
        // add table
        $(document).on('submit', '#table_type_add', function (e) {
            e.preventDefault();
            const table_type_add_form = $('#table_type_add').parsley();
            let table_type_add_form_data = new FormData($('#table_type_add')[0]);


            if (table_type_add_form.isValid()) {
                // is_active value set
                // if (table_type_add_form_data.has('image')) ($("input[name='image']").val() === '') ? table_type_add_form_data.delete('image') : '';
                if (!table_type_add_form_data.has('is_active')) table_type_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["table_type_list"],
                    type: "POST",
                    data: JSON.stringify({
                        "name": $('#name').val(),
                        "is_active": $('#is_active').is(":checked"),
                    }),
                    dataType: 'json',
                    contentType: "application/json",
                    success: function (resp) {
                        // Display a success message
                        notify("Table type has been created successfully.", "success");

                        // Delay the page refresh for 2 seconds (2000 milliseconds)
                        setTimeout(function() {
                            // Refresh the page
                            // location.reload();
                            window.location.href = table_type_list_url;
                        }, 2000); // Adjust the delay time as needed
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
    *                       Product edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit product form value setup
        $.ajax({
            url: `${api_urls["table_type_list"]}${uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#table_type_edit'), response.data);
            },
            error: function (response) {
                notify(`${response.responseJSON.message}`, 'error')
            }
        });
    };

    /*
    * =========================================================================
    *                       Menu type edit
    * =========================================================================
    **/

    edit = () => {
        // edit table
        $(document).on('submit', '#table_type_edit', function (e) {
            e.preventDefault();
            const table_type_edit_form = $('#table_type_edit').parsley();
            let table_type_edit_form_data = new FormData($('#table_type_edit')[0]);

            if (table_type_edit_form.isValid()) {
                if (!table_type_edit_form_data.has('is_active')) table_type_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["table_type_list"] + uuid + '/',
                    type: "PATCH",
                    data: JSON.stringify({
                        "name": $('#name').val(),
                        "is_active": $('#is_active').is(":checked"),
                    }),
                    dataType: 'json',
                    contentType: "application/json",
                    success: function (response) {
                        notify("Success", 'success')
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
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        this.select_sidebar_option()
        this.list();
        if (page_type === "add") {
        this.add();
        }
        if (page_type === "edit") {
            this.edit_form_value_set();
            this.edit();
        }
    }
}


new MenuType().main();