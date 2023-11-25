/*
* =============================================================================
*                             MANUFACTUR INVOICE
* =============================================================================
**/

class Manufacturer {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_order_management_a').click();
        $('#sidebar_option_order_management_manufacturer_invoice').addClass('active');
    };

    /*
    * =========================================================================
    *                      Manufacturer in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dealerDataTable').DataTable({
            "processing": true,
            "serverSide": true,
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
                'url': dealer_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function(row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "Name", "data": "name"},
                {"title": "Email", "data": "email"},
                {"title": "Phone", "data": "phone"},
                {"title": "Company Name", "data": "company_name"},
                {"title": "Company Email", "data": "company_email"}
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

        // Single click row select the row and mark a different color
        $('#dealerDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dealerDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       Available Manufacturer Invoice in Datatable
    * =========================================================================
    **/
    available_invoice_list = () => {
        let self = this;

        let table = $('#manufacturerInvoiceDataTable').DataTable({
            "processing": false,
            "serverSide": false,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add Invoice',
                    attr: {
                        title: 'Add Manufacturer Invoice',
                        id: 'addManufacturerInvoiceButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        (async () => {
                            const { value: file } = await Swal.fire({
                              title: 'Select a pdf file',
                              // input: 'file',
                              // inputAttributes: {
                              //   'accept': '.pdf',
                              //   'aria-label': 'Upload manufacturer invoice'
                              // },
                              html:
                                '<input id="swal-distributor" class="swal2-input" placeholder="Enter distributor name">' +
                                '<select id="swal-manufacturer" class="swal2-input"></select>' +
                                ' <br><br><input  id="swal-file" type="file" accept=".pdf" aria-label="Upload manufacturer invoice">',
                              showCancelButton: true,
                              confirmButtonColor: '#3085d6',
                              cancelButtonColor: '#d33',
                              confirmButtonText: 'Upload'
                            });

                            if (file) {
                                let formData = new FormData();
                                formData.append('distributor', $('#swal-distributor').val());
                                formData.append('manufacturer', $('#swal-manufacturer').val());
                                formData.append('invoice', $('#swal-file')[0].files[0]);

                                // do ajax request to upload csv file
                                $.blockUI();
                                $.ajax({
                                    url: manufacturer_invoice_api_url,
                                    type: "POST",
                                    data : formData,
                                    processData: false,  // tell jQuery not to process the data
                                    contentType: false,  // tell jQuery not to set contentType
                                    success: function (resp) {
                                        Swal.fire(
                                            'Uploaded!',
                                            'Manufacturer invoice uploaded successfully.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        $.unblockUI();
                                        notify(response.responseJSON.details, 'error')
                                    },
                                    complete: function (response) {
                                        $.unblockUI()
                                    }
                                });
                            }
                        })()
                        
                        $("#swal-manufacturer").select2({
                            placeholder: "Select a manufacturer",
                            allowClear: true,
                            minimumInputLength: 3,
                            dropdownParent: $('.swal2-container'),
                            ajax: {
                                url: '/api/v1/brand/search/',
                                dataType: 'json',
                                processResults: function (data) {
                                    // Transforms the top-level key of the response object from 'items' to 'results'
                                    let results = []
                                    $.each(data.data, function(i, v) {
                                        results.push({
                                            id: v.id,
                                            text: v.name,
                                            other: v
                                        })
                                    })
                                    return {
                                        results: results
                                    };
                                }
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
                // {
                //     extend: 'print',
                //     title: 'USERS',
                //     messageTop: '<h5 class="text-center">User List</h5>',
                //     messageBottom: null
                // }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': manufacturer_invoice_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function(row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('data-manufacturer_invoice_id', data.uuid);
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "Invoice", "data": "invoice"},
                {"title": "Distributor", "data": "distributor"},
                {"title": "Manufacturer", "data": "manufacturer_name"},
                {"title": "Delete", "data": ""},
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
                        return `<a href="/media/${data}" target="_blank">Invoice</a>`;
                    }
                },
                {
                    targets: 4,
                    render: function (data, type, row, meta) {
                        return `<i class="fas fa-trash" style="color: #4e73df" id="${row.uuid}"></i>`;
                    }
                },
            ],
        });
    };

    /*
    * =========================================================================
    *                       Manufacturer Invoice Delete
    * =========================================================================
    **/

    delete = () => {
        // edit user
        $(document).on('click', '.fa-trash', function (e) {
            // e.preventDefault();
            let manufacturer_invoice_id = $(this).parent().parent().data('manufacturer_invoice_id');

            // submit an ajax request to the api endpoint
            $.ajax({
                url: manufacturer_invoice_api_url + `${manufacturer_invoice_id}/`,
                type: "DELETE",
                success: function (resp) {
                    notify('Deletion successful', 'success');
                    window.location.reload();
                },
                error: function (response) {
                    if (response.status === 422) {
                        let errors = '';
                        $.map(response.responseJSON.details, function (v, i) {
                            $.each(v, function (j, k) {
                                errors += `<li>${i}: ${k}</l1>`;
                            })
                        });
                        let final_error = `<ul>${errors}</ul>`;

                        $('.failed')
                            .html(final_error)
                            .css('display', 'block')
                    }
                }
            });
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
        // this.list();
        this.available_invoice_list();
        this.delete();
    }
}


new Manufacturer().main();
