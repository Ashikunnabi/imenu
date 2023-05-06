/*
* =============================================================================
*                                   EXPENSE TYPE    
* =============================================================================
**/

class ExpenseType {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_others_a').click();
        $('#sidebar_option_others_expense_type').addClass('active');
    };

    /*
    * =========================================================================
    *                       EXPENSE TYPE in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#expenseTypeDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add New expense type',
                        id: 'addExpenseTypeButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        (async () => {
                            const { value: file } = await Swal.fire({
                              title: 'Create expense type',
                              html:
                                `<div style="text-align:left">
                                    <lable>Name</lable>
                                    <input type="text" placeholder="" id="swal-name">
                                </div>`,
                              showCancelButton: true,
                              confirmButtonColor: '#3085d6',
                              cancelButtonColor: '#d33',
                              confirmButtonText: 'Create'
                            });

                            if (file) {
                                let formData = new FormData();
                                
                                formData.append('name', $("#swal-name").val());

                                // do ajax request
                                $.blockUI();
                                $.ajax({
                                    url: expense_type_api_url,
                                    type: "POST",
                                    data : formData,
                                    processData: false,  // tell jQuery not to process the data
                                    contentType: false,  // tell jQuery not to set contentType
                                    success: function (resp) {
                                        Swal.fire(
                                            'Created!',
                                            'Expense type created successfully.',
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
                    text: 'Delete',
                    attr: {
                        title: 'Delete Expense Type',
                        id: 'deleteExpenseTypeButton',
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
                                let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
                                // do ajax request to delete
                                $.ajax({
                                    url: expense_type_api_url + data[0].uuid + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Expense type has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
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
                                        notify(response.responseJSON.detail, 'error');
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
                // {
                //     extend: 'print',
                //     title: 'USERS',
                //     messageTop: '<h5 class="text-center">User List</h5>',
                //     messageBottom: null
                // }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': expense_type_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "Name", "data": "name"},
                {"title": "Created At", "data": "created_at"},
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return `${moment(data).format('YYYY-MM-DD')}`
                    },
                },
            ],
        });

        // Single click row select the row and mark a different color
        $('#expenseTypeDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
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
    }
}

new ExpenseType().main();
