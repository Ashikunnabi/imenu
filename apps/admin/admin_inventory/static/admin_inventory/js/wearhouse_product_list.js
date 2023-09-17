/*
* =============================================================================
*                                   SUPPLIER
* =============================================================================
**/

class warehouseProduct {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_inventory_a').click();
        $('#sidebar_option_inventory_warehouse').addClass('active');
    };

    /*
    * =========================================================================
    *                       warehouse in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;
        var urlParams = new URLSearchParams(window.location.search);

        let table = $('#warehouseProductDataTable').DataTable({
            "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
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
                'url': warehouse_product_api_url + `?warehouse=${urlParams.get('warehouse')}`,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "Product id", "data": "product_details.product_id"},
                {"title": "Stock", "data": "stock"},
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                }
            ],
        });

        // Single click row select the row and mark a different color
        $('#warehouseDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#warehouseDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       warehouse add
    * =========================================================================
    **/

    add = () => {
        // add warehouse
        $(document).on('submit', '#warehouse_add', function (e) {
            e.preventDefault();
            const warehouse_add_form = $('#warehouse_add').parsley();
            let warehouse_add_form_data = new FormData($('#warehouse_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (warehouse_add_form.isValid()) {
                // is_active value set
                if (warehouse_add_form_data.has('image')) ($("input[name='image']").val() === '') ? warehouse_add_form_data.delete('image') : '';
                if (!warehouse_add_form_data.has('is_active')) warehouse_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: warehouse_api_url,
                    headers: {"X-CSRFToken": csrf_token},
                    type: "POST",
                    data: warehouse_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = warehouse_list_url;
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
    *                       warehouse edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit warehouse form value setup
        $.ajax({
            url: warehouse_api_url + uuid,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'image') (value != null) ? $('#editwarehouseCurrentImage').attr('href', `/media/${value}`) : "";
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#warehouse_edit'), response);
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
    *                       warehouse edit
    * =========================================================================
    **/

    edit = () => {
        // edit warehouse
        $(document).on('submit', '#warehouse_edit', function (e) {
            e.preventDefault();
            const warehouse_edit_form = $('#warehouse_edit').parsley();
            let warehouse_edit_form_data = new FormData($('#warehouse_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (warehouse_edit_form.isValid()) {
                // remove image attribute if no image uploaded
                if (warehouse_edit_form_data.has('image')) ($("input[name='image']").val() === '') ? warehouse_edit_form_data.delete('image') : '';
                if (!warehouse_edit_form_data.has('is_active')) warehouse_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: warehouse_api_url + uuid + '/',
                    headers: {"X-CSRFToken": csrf_token},
                    type: "PATCH",
                    data: warehouse_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.reload();
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
        // this.add();
        // this.edit_form_value_set();
        // this.edit();
    }
}


new warehouseProduct().main();
