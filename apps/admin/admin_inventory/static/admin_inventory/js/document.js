/*
* =============================================================================
*                                   BRAND
* =============================================================================
**/

class Document {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_inventory_a').click();
        $('#sidebar_option_inventory_document').addClass('active');
    };

    /*
    * =========================================================================
    *                       Document in Datatable
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
                        title: 'Add document',
                        id: 'addDocumentButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = document_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete document',
                        id: 'deleteDocumentButton',
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
                                    url: api_urls["document_list"] + data[0].uuid + '/',
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
                'url': api_urls["document_list"],
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
                { "title": "Extension", "data": "extension" },
                { "title": "Encrypted", "data": "is_encrypted" },
                { "title": "View", "data": "path" },
                { "title": "Active", "data": "is_active" },
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
                {
                    "targets": [4],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        if ([null, ""].indexOf(data)) return '';
                        return `<a href="/media/${data}" target="_blank">Document</a>`;
                    },
                },
                
                {
                    "targets": [5],
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
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       Document add
    * =========================================================================
    **/

    add = () => {
        // add document
        $(document).on('submit', '#document_add', function (e) {
            e.preventDefault();
            const document_add_form = $('#document_add').parsley();
            let document_add_form_data = new FormData($('#document_add')[0]);


            if (document_add_form.isValid()) {
                // is_active value set
                if (document_add_form_data.has('document')) ($("input[name='document']").val() === '') ? document_add_form_data.delete('document') : '';
                if (!document_add_form_data.has('is_active')) document_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["document_list"],
                    type: "POST",
                    data: document_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = document_list_url;
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
    *                       Document edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit document form value setup
        $.ajax({
            url: api_urls["document_list"] + uuid,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'document') (value != null) ? $('#editDocumentCurrentDocument').attr('href', `/media/${value}`) : "";
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#document_edit'), response.data);
            },
            error: function (response) {
                notify(`${response.responseJSON.message}`, 'error')
            }
        });
    };

    /*
    * =========================================================================
    *                       Document edit
    * =========================================================================
    **/

    edit = () => {
        // edit document
        $(document).on('submit', '#document_edit', function (e) {
            e.preventDefault();
            const document_edit_form = $('#document_edit').parsley();
            let document_edit_form_data = new FormData($('#document_edit')[0]);

            if (document_edit_form.isValid()) {
                // remove document attribute if no document uploaded
                if (document_edit_form_data.has('document')) ($("input[name='document']").val() === '') ? document_edit_form_data.delete('document') : '';
                if (!document_edit_form_data.has('is_active')) document_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["document_list"] + uuid + '/',
                    type: "PATCH",
                    data: document_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
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
        // call this function to execute all operations of this class
        this.select_sidebar_option();
        if (page_type === "list") this.list();
        if (page_type === "add") this.add();
        if (page_type === "edit") {
            this.edit_form_value_set();
            this.edit();
        }
    }
}


new Document().main();
