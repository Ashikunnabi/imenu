/*
* =============================================================================
*                                   PRODUCT UNIT
* =============================================================================
**/

export class ProductUnit {

    /*
    * =========================================================================
    *                       Product in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTableProductUnit').DataTable({
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
                            title: 'Add Product Unit',
                            html: `
                            <form id="product_unit" data-parsley-validate>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="name" class="font-weight-bold">Unit: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <select class="form-control" id="unit_uuid" name="unit_uuid" required></select>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="min" class="font-weight-bold">Min: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="text" class="form-control font-weight-bold" id="add_min" name="min" data-parsley-maxlength="50"
                                            placeholder="max 50 chars" required>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="max" class="font-weight-bold">Max: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="text" class="form-control font-weight-bold" id="add_max" name="max" data-parsley-maxlength="50"
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
                                    url: api_urls["product_unit_list"],
                                    data: JSON.stringify({
                                        "unit_uuid": $("#unit_uuid").val(),
                                        "min": $("#add_min").val(),
                                        "max": $("#add_max").val(),
                                    }),
                                    type: "POST",
                                    contentType: "application/json",
                                    success: function (response) {
                                        Swal.fire(
                                            'Success!',
                                            'Unit has been added.',
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
                        self.unit_search();
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
                                    url: api_urls["product_unit_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Unit has been deleted.',
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
                'url': api_urls["product_unit_list"],
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
                { "title": "Name", "data": "unit.name" },
                { "title": "Min", "data": "min" },
                { "title": "Max", "data": "max" },
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
        $('#dataTableProductUnit tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTableProductUnit tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            self.edit_form_value_set(table, data.uuid);
        });
    };

    /*
    * =========================================================================
    *                       UNIT SEARCH
    * =========================================================================
    **/
    unit_search = (default_value = null) => {
        $("#unit_uuid").select2({
            dropdownParent: $("#product_unit"),
            allowClear: true,
            placeholder: "Select unit",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["unit_list"],
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
            $('#unit_uuid').append(newOption).trigger('change');
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
            url: `${api_urls["product_unit_list"]}${_uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        console.log(key, value)
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                Swal.fire({
                    title: 'Edit Product Unit',
                    html: `
                <form id="product_unit" data-parsley-validate>
                    <div class="row">
                        <div class="col-4">
                            <label for="name" class="font-weight-bold">Unit: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <select class="form-control" id="unit_uuid" name="unit_uuid" required></select>
                        </div>
                    </div>
                    <br>
                    <div class="row">
                        <div class="col-4">
                            <label for="min" class="font-weight-bold">Min: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="text" class="form-control font-weight-bold" id="edit_min" name="min" data-parsley-maxlength="50"
                                placeholder="max 50 chars" required>
                        </div>
                    </div>
                    <br>
                    <div class="row">
                        <div class="col-4">
                            <label for="max" class="font-weight-bold">Max: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="text" class="form-control font-weight-bold" id="edit_max" name="max" data-parsley-maxlength="50"
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
                            url: `${api_urls["product_unit_list"]}${_uuid}/`,
                            data: JSON.stringify({
                                "unit_uuid": $("#unit_uuid").val(),
                                "min": $("#edit_min").val(),
                                "max": $("#edit_max").val(),
                            }),
                            type: "PUT",
                            contentType: "application/json",
                            success: function (response) {
                                Swal.fire(
                                    'Success!',
                                    'Unit has been updated.',
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

                populate($('#product_unit'), response.data);

                // Select2 unit value set
                if (response.data.unit) {
                    let default_value = {
                        "id": response.data.unit.uuid,
                        "text": response.data.unit.name,
                    }
                    self.unit_search(default_value = default_value);
                } else {
                    self.unit_search();
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
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        if (page_type === "edit") {
            this.list();
        }
    }
}
