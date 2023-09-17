/*
* =============================================================================
*                                   PRODUCT DOCUMENT
* =============================================================================
**/

export class ProductDocument {

    /*
    * =========================================================================
    *                       Product in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTableProductDocument').DataTable({
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
                            title: 'Add Product Document',
                            html: `
                            <form id="product_document_add" data-parsley-validate>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="add_document" class="font-weight-bold">Document: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="file" class="form-control font-weight-bold" id="add_document" name="file" required>
                                    </div>
                                </div>
                                <br>
                                <div class="row">
                                    <div class="col-4">
                                        <label for="add_sort_order" class="font-weight-bold">Sort Order: <span class="text-danger">*</span></label>
                                    </div>
                                    <div class="col-8">
                                        <input type="number" class="form-control font-weight-bold" id="add_sort_order" name="sort_order" data-parsley-maxlength="50"
                                            placeholder="max 50 chars" required value="1">
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
                                let formData = new FormData();
                                formData.append('file', $('#add_document')[0].files[0]);
                                formData.append('sort_order', $('#add_sort_order').val());
                                $.ajax({
                                    url: api_urls["product_document_upload"],
                                    type: "POST",
                                    data : formData,
                                    processData: false,  // tell jQuery not to process the data
                                    contentType: false,  // tell jQuery not to set contentType
                                    success: function (response) {
                                        Swal.fire(
                                            'Success!',
                                            'Document has been added.',
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
                        title: 'Delete document',
                        id: 'deleteProductDocumentButton',
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
                                    url: api_urls["product_document_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Document has been deleted.',
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
                'url': api_urls["product_document_list"],
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
                { "title": "Document", "data": "document.file" },
                { "title": "View", "data": "document.file" },
                { "title": "Sort Order", "data": "sort_order" },
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
                    targets: 2,
                    render: function (data, type, row, meta) {
                        if (!data) return
                        let width = "100%";
                        let height = "100%";
                        if (row.type === "qrcode") {
                            width = "100px";
                            height = "100px";
                        }
                        if (row.type === "image") {
                            width = "300px";
                            height = "300px";
                        }
                        let html = `<img src="${data}" width="${width}" height="${height}">`
                        return html
                    }
                },
                {
                    targets: 3,
                    render: function (data, type, row, meta) {
                        if (!data) return
                        let html = `<a href="${data}" target="_blank">View File</a>`
                        return html
                    }
                },
            ],
        });

        // Single click row select the row and mark a different color
        $('#dataTableProductDocument tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTableProductDocument tbody').on('dblclick', 'tr', function () {
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
            url: `${api_urls["product_document_list"]}${_uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        if (key === 'document') $('input[name=document]').val(value.uuid);
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                Swal.fire({
                    title: 'Edit Product Document',
                    html: `
                <form id="product_document_edit" data-parsley-validate>
                    <div class="row">
                        <div class="col-4">
                            <label for="edit_sort_order" class="font-weight-bold">Sort Order: <span class="text-danger">*</span></label>
                        </div>
                        <div class="col-8">
                            <input type="number" class="form-control font-weight-bold" id="edit_sort_order" name="sort_order" data-parsley-maxlength="50"
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
                            url: `${api_urls["product_document_list"]}${_uuid}/`,
                            data: JSON.stringify({
                                "sort_order": $("#edit_sort_order").val(),
                            }),
                            type: "PUT",
                            contentType: "application/json",
                            success: function (response) {
                                Swal.fire(
                                    'Success!',
                                    'Document has been updated.',
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

                populate($('#product_document_edit'), response.data);
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
