/*
* =============================================================================
*                                   PRODUCT VAT
* =============================================================================
**/

export class ProductVat {

    /*
    * =========================================================================
    *                       Product in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTableProductVat').DataTable({
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
                            title: 'Add Product Vat',
                            html: `
                            <form id="product_vat" data-parsley-validate>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="name" class="font-weight-bold">Vat: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <select class="form-control" id="vat_uuid" name="vat_uuid" required></select>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="flat" class="font-weight-bold">Flat: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="text" class="form-control font-weight-bold" id="add_flat" name="flat" data-parsley-maxlength="50"
                                            placeholder="max 50 chars" required>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="percentage" class="font-weight-bold">Percentage: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="text" class="form-control font-weight-bold" id="add_percentage" name="percentage" data-parsley-maxlength="50"
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
                                    url: api_urls["product_vat_list"],
                                    data: JSON.stringify({
                                        "vat_uuid": $("#vat_uuid").val(),
                                        "flat": $("#add_flat").val(),
                                        "percentage": $("#add_percentage").val(),
                                    }),
                                    type: "POST",
                                    contentType: "application/json",
                                    success: function (response) {
                                        Swal.fire(
                                            'Success!',
                                            'Vat has been added.',
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
                        self.vat_search();
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
                                    url: api_urls["product_vat_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Vat has been deleted.',
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
                'url': api_urls["product_vat_list"],
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
                { "title": "Name", "data": "vat.name" },
                { "title": "Flat", "data": "flat" },
                { "title": "Percentage", "data": "percentage" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
            ],
        });
        self.table = table

        // Single click row select the row and mark a different color
        $('#dataTableProductVat tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTableProductVat tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            self.edit_form_value_set(table, data.uuid);
        });
    };

    /*
    * =========================================================================
    *                       VAT SEARCH
    * =========================================================================
    **/
    vat_search = (default_value = null) => {
        $("#vat_uuid").select2({
            dropdownParent: $("#product_vat"),
            allowClear: true,
            placeholder: "Select vat",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["vat_list"],
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
            $('#vat_uuid').append(newOption).trigger('change');
            console.log(default_value)
        }
    }


    /*
    * =========================================================================
    *                       Product edit form setup
    * =========================================================================
    **/

    edit_form_value_set = (data_table, _uuid) => {
        // edit product form value setup
        let self = this
        $.ajax({
            url: `${api_urls["product_vat_list"]}${_uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                Swal.fire({
                    title: 'Edit Product Vat',
                    html: `
                <form id="product_vat" data-parsley-validate>
                    <div class="row">
                        <div class="col-4">
                            <label for="name" class="font-weight-bold">Vat: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <select class="form-control" id="vat_uuid" name="vat_uuid" required></select>
                        </div>
                    </div>
                    <br>
                    <div class="row">
                        <div class="col-4">
                            <label for="flat" class="font-weight-bold">Flat: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="text" class="form-control font-weight-bold" id="edit_flat" name="flat" data-parsley-maxlength="50"
                                placeholder="max 50 chars" required>
                        </div>
                    </div>
                    <br>
                    <div class="row">
                        <div class="col-4">
                            <label for="percentage" class="font-weight-bold">Percentage: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="text" class="form-control font-weight-bold" id="edit_percentage" name="percentage" data-parsley-maxlength="50"
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
                            url: `${api_urls["product_vat_list"]}${_uuid}/`,
                            data: JSON.stringify({
                                "vat_uuid": $("#vat_uuid").val(),
                                "flat": $("#edit_flat").val(),
                                "percentage": $("#edit_percentage").val(),
                            }),
                            type: "PUT",
                            contentType: "application/json",
                            success: function (response) {
                                Swal.fire(
                                    'Success!',
                                    'Vat has been updated.',
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

                populate($('#product_vat'), response.data);

                // Select2 vat value set
                if (response.data.vat) {
                    let default_value = {
                        "id": response.data.vat.uuid,
                        "text": response.data.vat.name,
                    }
                    self.vat_search(default_value = default_value);
                } else {
                    self.vat_search();
                }
            },
            error: function (response) {
                notify(`${response.responseJSON.message}`, 'error')
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
