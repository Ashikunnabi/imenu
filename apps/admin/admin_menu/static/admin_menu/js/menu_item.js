/*
* =============================================================================
*                                   MENU ITEM
* =============================================================================
**/

export class MenuItem {

    /*
    * =========================================================================
    *                       MenuItem in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTableMenuItem').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add menu item',
                        id: 'addMenuItemButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        Swal.fire({
                            title: 'Add Item',
                            html: `
                            <form id="menu_item_add" data-parsley-validate>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="add__menu_item__uuid" class="font-weight-bold">Item: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <select class="form-control" id="add__menu_item__uuid" name="add__menu_item__uuid" required></select>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="add__menu_item__start_at" class="font-weight-bold">Start At: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="date" class="form-control font-weight-bold" id="add__menu_item__start_at" name="add__menu_item__start_at" data-parsley-maxlength="50"
                                            placeholder="max 50 chars" required>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="add__menu_item__end_at" class="font-weight-bold">End At: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="date" class="form-control font-weight-bold" id="add__menu_item__end_at" name="add__menu_item__end_at" data-parsley-maxlength="50"
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
                                    url: api_urls["menu_item_list"],
                                    data: JSON.stringify({
                                        "menu_uuid": uuid,
                                        "item_uuid": $("#add__menu_item__uuid").val(),
                                        "start_at": moment($("#add__menu_item__start_at").val()).format(),
                                        "end_at": moment($("#add__menu_item__end_at").val()).format(),
                                    }),
                                    type: "POST",
                                    contentType: "application/json",
                                    success: function (response) {
                                        Swal.fire(
                                            'Success!',
                                            'Item has been added.',
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

                        self.item_search();
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete Item',
                        id: 'deleteMenuItemButton',
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
                                    url: api_urls["menu_item_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Item has been deleted from the menu.',
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
                'url': api_urls["menu_item_list"],
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
                { "title": "Item", "data": "item.name" },
                { "title": "Start At", "data": "start_at" },
                { "title": "End At", "data": "end_at" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    targets: 2,
                    render: function (data, type, row, meta) {
                        return moment(data).format('LLL')
                    }
                },
                {
                    targets: 3,
                    render: function (data, type, row, meta) {
                        return moment(data).format('LLL')
                    }
                },
            ],
        });

        // Single click row select the row and mark a different color
        $('#dataTableMenuItem tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTableMenuItem tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            self.edit_form_value_set(table, data.uuid);
        });
    };

    /*
    * =========================================================================
    *                       MenuItem edit form setup
    * =========================================================================
    **/

    edit_form_value_set = (data_table, _uuid) => {
        // edit product form value setup
        let self = this
        $.ajax({
            url: `${api_urls["menu_item_list"]}${_uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'start_at') $('#edit__menu_item__start_at').val(moment(value).format('YYYY-MM-DD'));
                        else if (key === 'end_at') $('#edit__menu_item__end_at').val(moment(value).format('YYYY-MM-DD'));
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                Swal.fire({
                    title: 'Edit Item',
                    html: `
                    <form id="menu_item_edit" data-parsley-validate>
                        <div class="row">
                            <div class="col-4">
                                <label for="edit__menu_item__uuid" class="font-weight-bold">Item: <span class="text-danger">*</span></label>
                            </div>
                            <div class="col-8">
                                <select class="form-control" id="edit__menu_item__uuid" name="edit__menu_item__uuid" required></select>
                            </div>
                        </div>
                        <br>
                        <div class="row">
                            <div class="col-4">
                                <label for="edit__menu_item__start_at" class="font-weight-bold">Start At: <span class="text-danger">*</span></label>
                            </div>
                            <div class="col-8">
                                <input type="date" class="form-control font-weight-bold" id="edit__menu_item__start_at" name="edit__menu_item__start_at" data-parsley-maxlength="50"
                                    placeholder="max 50 chars" required>
                            </div>
                        </div>
                        <br>
                        <div class="row">
                            <div class="col-4">
                                <label for="edit__menu_item__end_at" class="font-weight-bold">End At: <span class="text-danger">*</span></label>
                            </div>
                            <div class="col-8">
                                <input type="date" class="form-control font-weight-bold" id="edit__menu_item__end_at" name="edit__menu_item__end_at" data-parsley-maxlength="50"
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
                            url: `${api_urls["product_warehouse_list"]}${_uuid}/`,
                            data: JSON.stringify({
                                "product_uuid": uuid,
                                "warehouse_uuid": $("#edit_warehouse").val(),
                                "stock": $("#edit_stock").val(),
                            }),
                            type: "PUT",
                            contentType: "application/json",
                            success: function (response) {
                                Swal.fire(
                                    'Success!',
                                    'Warehouse has been updated.',
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

                populate($('#menu_item_edit'), response.data);

                // Select2 item value set
                if (response.data.item) {
                    let default_value = {
                        "id": response.data.item.uuid,
                        "text": response.data.item.name,
                    }
                    self.item_search("edit__menu_item__uuid", default_value = default_value);
                } else {
                    self.item_search("edit__menu_item__uuid");
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
    *                       MENU ITEM SEARCH
    * =========================================================================
    **/
    item_search = (element_id = "add__menu_item__uuid", default_value = null) => {
        let dropdownParent = "#menu_item_add"
        if (element_id == "edit__menu_item__uuid") dropdownParent = "#menu_item_edit";

        $(`#${element_id}`).select2({
            dropdownParent: $(dropdownParent),
            allowClear: true,
            placeholder: "Select menu item",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["product_list"],
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
            $(`#${element_id}`).append(newOption).trigger('change');
        }
    }

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
