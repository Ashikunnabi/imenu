/*
* =============================================================================
*                             FINALE INVOICE
* =============================================================================
**/

class Dealer {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_order_management_a').click();
        $('#sidebar_option_order_management_finale_invoice').addClass('active');
    };

    /*
    * =========================================================================
    *                      Dealer in Datatable
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
    *                       Available Finale Invoice in Datatable
    * =========================================================================
    **/
    available_invoice_list = () => {
        let self = this;

        let table = $('#finaleInvoiceDataTable').DataTable({
            "processing": false,
            "serverSide": false,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add Invoice',
                    attr: {
                        title: 'Add Finale Invoice',
                        id: 'addFinaleInvoiceButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        (async () => {
                            const { value: file } = await Swal.fire({
                              title: 'Select a pdf file',
                              // input: 'file',
                              // inputAttributes: {
                              //   'accept': '.pdf',
                              //   'aria-label': 'Upload finale invoice'
                              // },
                              html:
                                '<input id="swal-tracking_number" class="swal2-input" placeholder="Enter tracking number">' +
                                '<input id="swal-tracking_number_added_at" type="date" style="width:100%">' +
                                '<input  id="swal-file" type="file" class="swal2-file" accept=".pdf" aria-label="Upload finale invoice">',
                              showCancelButton: true,
                              confirmButtonColor: '#3085d6',
                              cancelButtonColor: '#d33',
                              confirmButtonText: 'Upload'
                            });

                            if (file) {
                                let formData = new FormData();
                                formData.append('tracking_number', $('#swal-tracking_number').val());
                                formData.append('tracking_number_added_at', $('#swal-tracking_number_added_at').val());
                                formData.append('invoice', $('#swal-file')[0].files[0]);
                                formData.append('dealer', uuid);

                                // do ajax request to upload csv file
                                $.blockUI();
                                $.ajax({
                                    url: finale_invoice_api_url,
                                    type: "POST",
                                    data : formData,
                                    processData: false,  // tell jQuery not to process the data
                                    contentType: false,  // tell jQuery not to set contentType
                                    success: function (resp) {
                                        Swal.fire(
                                            'Uploaded!',
                                            'Finale invoice uploaded successfully.',
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
                'url': finale_invoice_api_url + `?uuid=${uuid}`,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function(row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('data-finale_invoice_id', data.uuid);
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "Invoice", "data": "invoice"},
                {"title": "Tracking Number", "data": "tracking_number"},
                {"title": "Date (YYYY-MM-DD)", "data": "tracking_number_added_at"},
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
    *                       Finale Invoice Delete
    * =========================================================================
    **/

    delete = () => {
        // edit user
        $(document).on('click', '.fa-trash', function (e) {
            // e.preventDefault();
            let finale_invoice_id = $(this).parent().parent().data('finale_invoice_id');

            // submit an ajax request to the api endpoint
            $.ajax({
                url: finale_invoice_api_url + `${finale_invoice_id}/`,
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
        this.list();
        this.available_invoice_list();
        this.delete();
    }
}


new Dealer().main();
