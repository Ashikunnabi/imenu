/*
* =============================================================================
*                                   PRODUCT PRICE
* =============================================================================
**/

export class ProductPrice {

    /*
    * =========================================================================
    *                       Product in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTableProductPrice').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add product',
                        id: 'addProductButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        Swal.fire({
                            title: 'Add Product Price',
                            html: `
                            <form id="product_price_add" data-parsley-validate>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="type" class="font-weight-bold">Type: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="text" class="form-control font-weight-bold" id="add_type" name="type" data-parsley-maxlength="50"
                                            placeholder="max 50 chars" required>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="value" class="font-weight-bold">Price: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="text" class="form-control font-weight-bold" id="add_value" name="value" data-parsley-maxlength="50"
                                            placeholder="max 50 chars" required>
                                    </div>
                                </div>
                            </form>
                            
                            `,
                            icon: '',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Save'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                $.ajax({
                                    url: api_urls["product_price_list"],
                                    data: JSON.stringify({
                                        "type": $("#add_type").val(),
                                        "price": $("#add_value").val(),
                                    }),
                                    type: "POST",
                                    contentType: "application/json",
                                    success: function (response) {
                                        Swal.fire(
                                            'Success!',
                                            'Price has been added.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        $.each(response.responseJSON.error, function (i, v) {
                                            notify(`${i.toUpperCase()} - ${v}`, 'error')
                                        })
                                    }
                                });
                            }
                        })
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete product',
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
                                $.ajax({
                                    url: api_urls["product_price_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Price has been deleted.',
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
                'url': api_urls["product_price_list"],
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
                { "title": "Type", "data": "type" },
                { "title": "Price", "data": "price" },
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
                        return data.toUpperCase()
                    }
                },
            ],
        });
        self.table = table

        // Single click row select the row and mark a different color
        $('#dataTableProductPrice tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTableProductPrice tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            self.edit_form_value_set(table, data.uuid);
        });
    };

    /*
    * =========================================================================
    *                       Product edit form setup
    * =========================================================================
    **/

    edit_form_value_set = (data_table, _uuid) => {
        // edit product form value setup
        $.ajax({
            url: `${api_urls["product_price_list"]}${_uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                Swal.fire({
                    title: 'Edit Product Price',
                    html: `
                <form id="product_price_edit" data-parsley-validate>
                    <div class="row">
                        <div class="col-4">
                            <label for="type" class="font-weight-bold">Type: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="text" class="form-control font-weight-bold" id="edit_type" name="type" data-parsley-maxlength="50"
                                placeholder="max 50 chars" required>
                        </div>
                    </div>
                    <br>
                    <div class="row">
                        <div class="col-4">
                            <label for="value" class="font-weight-bold">Price: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="text" class="form-control font-weight-bold" id="edit_value" name="price" data-parsley-maxlength="50"
                                placeholder="max 50 chars" required>
                        </div>
                    </div>
                </form>
                
                `,
                    icon: '',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Save'
                }).then((result) => {
                    if (result.isConfirmed) {
                        $.ajax({
                            url: `${api_urls["product_price_list"]}${_uuid}/`,
                            data: JSON.stringify({
                                "type": $("#edit_type").val(),
                                "price": $("#edit_value").val(),
                            }),
                            type: "PUT",
                            contentType: "application/json",
                            success: function (response) {
                                Swal.fire(
                                    'Success!',
                                    'Price has been updated.',
                                    'success'
                                );
                                data_table.ajax.reload()
                            },
                            error: function (response) {
                                $.each(response.responseJSON.error, function (i, v) {
                                    notify(`${i.toUpperCase()} - ${v}`, 'error')
                                })
                            }
                        });
                    }
                })

                populate($('#product_price_edit'), response.data);
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
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        if (page_type === "edit") {
            this.list();
        }
    }
}
