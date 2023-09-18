/*
* =============================================================================
*                                   PRODUCT CODE
* =============================================================================
**/

export class ProductCode {

    /*
    * =========================================================================
    *                       Product in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTableProductCode').DataTable({
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
                            title: 'Add Product Code',
                            html: `
                            <form id="product_code_add" data-parsley-validate>
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
                                        <label for="value" class="font-weight-bold">Value: <span class="text-danger">*</span></label>
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
                                    url: api_urls["product_code_list"],
                                    data: JSON.stringify({
                                        "product_uuid": uuid,
                                        "type": $("#add_type").val(),
                                        "value": $("#add_value").val(),
                                    }),
                                    type: "POST",
                                    contentType: "application/json",
                                    success: function (response) {
                                        Swal.fire(
                                            'Success!',
                                            'Code has been added.',
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
                                    url: api_urls["product_code_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Code has been deleted.',
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
                'url': api_urls["product_code_list"],
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
                { "title": "Value", "data": "value" },
                { "title": "QR Code", "data": "" },
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
                {
                    targets: 3,
                    render: function (data, type, row, meta) {
                        let qr_code_path = ""
                        if (row.qr_code_path) {
                            qr_code_path = `
                            <a href="${row.qr_code_path}" class="d-none d-sm-inline-block btn btn-sm btn-secondary shadow-sm" target="_blank"><i class="fa fa-qrcode"></i></a>
                            `
                        }
                        let html = `
                            <a href="#" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm generate_qr_code">Generate</a>
                            ${qr_code_path}                            
                        `
                        return html
                    }
                },
            ],
        });
        self.table = table

        // Single click row select the row and mark a different color
        $('#dataTableProductCode tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTableProductCode tbody').on('dblclick', 'tr', function () {
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
            url: `${api_urls["product_code_list"]}${_uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                Swal.fire({
                    title: 'Edit Product Code',
                    html: `
                <form id="product_code_edit" data-parsley-validate>
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
                            <label for="value" class="font-weight-bold">Value: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="text" class="form-control font-weight-bold" id="edit_value" name="value" data-parsley-maxlength="50"
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
                            url: `${api_urls["product_code_list"]}${_uuid}/`,
                            data: JSON.stringify({
                                "product_uuid": uuid,
                                "type": $("#edit_type").val(),
                                "value": $("#edit_value").val(),
                            }),
                            type: "PUT",
                            contentType: "application/json",
                            success: function (response) {
                                Swal.fire(
                                    'Success!',
                                    'Code has been updated.',
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

                populate($('#product_code_edit'), response.data);
            },
            error: function (response) {
                notify(`${response.responseJSON.message}`, 'error')
            }
        });
    };

    /*
    * =========================================================================
    *                       Generate QR code
    * =========================================================================
    **/

    generate_qr_code = () => {
        let self = this
        $(document).on("click", ".generate_qr_code", function (e) {
            let tr = $(this).parent().parent();
            let data = self.table.row(tr).data();

            Swal.fire({
                title: 'Generate QR Code',
                html: `
                    <form id="add_product_code_qr_code" data-parsley-validate>
                        <div class="row">
                            <div class="col-2">
                                <label for="value" class="font-weight-bold">Value: <span class="text-danger">*</span></label>
                            </div>
                            <div class="col-10">
                                <!--<textarea id="add_product_code_qr_code_value" cols="30" rows="10">${JSON.stringify(data.value, null, 2)}</textarea>-->
                                <textarea id="add_product_code_qr_code_value" cols="30" rows="10">${data.value}</textarea>
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
                        url: `${api_urls["product_code_list"]}${data.uuid}/create-qr-code/`,
                        data: JSON.stringify({
                            "data": $("#add_product_code_qr_code_value").val(),
                        }),
                        type: "POST",
                        contentType: "application/json",
                        success: function (response) {
                            Swal.fire(
                                'Success!',
                                'QR Code has been generated.',
                                'success'
                            );
                            self.table.ajax.reload()
                        },
                        error: function (response) {
                            $.each(response.responseJSON.error, function (i, v) {
                                notify(`${i.toUpperCase()} - ${v}`, 'error')
                            })
                        }
                    });
                }
            })

        })
    };

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        if (page_type === "edit") {
            this.list();
            this.generate_qr_code();
        }
    }
}
