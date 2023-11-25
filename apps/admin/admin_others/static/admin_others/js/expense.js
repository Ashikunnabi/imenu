/*
* =============================================================================
*                                   EXPENSE
* =============================================================================
**/

class Expense {
    selected = [];
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_others_a').click();
        $('#sidebar_option_others_expense').addClass('active');
    };

    /*
    * =========================================================================
    *                       Expense in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;
        let table = $('#expenseDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B><"extra_btn">flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add expense',
                        id: 'addProductButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = expense_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete expense',
                        id: 'deleteProductButton',
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
                                    url: expense_api_url + data[0].uuid + '/',
                                    headers: { "X-CSRFToken": csrf_token },
                                    type: "DELETE",
                                    contentType: "application/json",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Expense has been deleted.',
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
                'url': expense_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function (row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
                if ($.inArray(data.DT_RowId, self.selected) !== -1) {
                    $(row).addClass('selected');
                }
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Expense Type", "data": "type_human_readable" },
                { "title": "Spender", "data": "spender_human_readable" },
                { "title": "Value", "data": "value" },
                { "title": "Description", "data": "description" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                // {
                //     "targets": [8],
                //     "visible": true,
                //     "searchable": true,
                //     "render": function (data, type, row, meta) {
                //         if (data) return 'Active';
                //         return 'Inactive'
                //     },
                // },
            ],
        });

        // Single click row select the row and mark a different color
        $('#expenseDataTable tbody').on('click', 'tr', function () {
            var id = this.id;
            var index = $.inArray(id, self.selected);

            if (index === -1) {
                self.selected.push(id);
            } else {
                self.selected.splice(index, 1);
            }

            $(this).toggleClass('selected');
        });

        // double click row will redirect to edit selected row
        $('#expenseDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       Expense add
    * =========================================================================
    **/

    add = () => {
        // add product
        let self = this;
        self.set_data_in_dropdown('select[name=type]', expense_type_api_url, null, "data")
        self.set_data_in_dropdown('select[name=spender]', spender_api_url, null)
        // self.set_expense_type_in_dropdown('select[name=type]', null);
        // self.set_spender_in_dropdown('select[name=spender]', null);
    
        $(document).on('submit', '#expense_add', function (e) {
            e.preventDefault();
            const expense_add_form = $('#expense_add').parsley();
            let expense_add_form_data = new FormData($('#expense_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (expense_add_form.isValid()) {
                // is_active value set
                // if (expense_add_form_data.has('image')) ($("input[name='image']").val() === '') ? expense_add_form_data.delete('image') : '';
                
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: expense_api_url,
                    headers: { "X-CSRFToken": csrf_token },
                    type: "POST",
                    data: expense_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = expense_list_url;
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
    *                       Expense edit form setup
    * =========================================================================
    **/

    set_data_in_dropdown = (field_name, url, selected=null, lookup_from="", key_name="id", value_name="name") => {
        // get a list of available categories
        $.ajax({
            url: url,
            type: "get",
            success: function (response) {
                let options = '';
                let lookup = (lookup_from !== "") ? response[lookup_from]: response;

                $.each(lookup, function (i, v) {
                    if (selected === v.id) {
                        options += `<option value=${v[key_name]} selected>${v[value_name]}</option>`
                    } else {
                        options += `<option value=${v[key_name]}>${v[value_name]}</option>`;
                    }
                });
                $(field_name).append(options);
            },
            error: function (response) {
                notify(response.responseText, 'error')
            }
        });
    };

    edit_form_value_set = () => {
        // edit product form value
        let self = this;
        $.ajax({
            url: expense_api_url + uuid + "/",
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editProductCurrentImage').attr('href', `/media/${value}`) : "";
                        else if (key === 'type') { self.set_data_in_dropdown('select[name=type]', expense_type_api_url, value, "data") }
                        else if (key === 'spender') { self.set_data_in_dropdown('select[name=spender]', spender_api_url, value) }
                        // else if (key === 'show_at_homepage_category') (value === true) ? $('input[name=show_at_homepage_category]').click() : "";
                        // else if (key === 'sync_from_finale') (value === true) ? $('input[name=sync_from_finale]').click() : "";
                        // else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#expense_edit'), response);
            },
            error: function (response) {
                notify(response.responseText, 'error')
            }
        });
    };

    /*
    * =========================================================================
    *                       Product edit
    * =========================================================================
    **/

    edit = () => {
        // edit product
        $(document).on('submit', '#expense_edit', function (e) {
            e.preventDefault();
            const expense_edit_form = $('#expense_edit').parsley();
            let expense_edit_form_data = new FormData($('#expense_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (expense_edit_form.isValid()) {
                // if (!product_edit_form_data.has('show_at_homepage_category')) product_edit_form_data.append('show_at_homepage_category', 0);
                // if (!product_edit_form_data.has('sync_from_finale')) product_edit_form_data.append('sync_from_finale', 0);
                // if (!product_edit_form_data.has('is_active')) product_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: expense_api_url + uuid + '/',
                    headers: { "X-CSRFToken": csrf_token },
                    type: "PATCH",
                    data: expense_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.reload();
                    },
                    error: function (response) {
                        notify(response.responseText, 'error')
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

        if (page === 'list') this.list();
        if (page === 'add') this.add();
        if (page === 'edit') {
            this.edit_form_value_set();
            this.edit();
        }
    }
}


new Expense().main();