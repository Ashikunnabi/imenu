/*
* =============================================================================
*                                   DEALER
* =============================================================================
**/

class Dealer {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_user_management_a').click();
        $('#sidebar_option_dealer_management_dealer').addClass('active');
    };

    /*
    * =========================================================================
    *                       Dealer in Datatable
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
    *                       Available Brands in Datatable
    * =========================================================================
    **/
    available_brand_list = () => {
        let self = this;

        let table = $('#brandDataTable').DataTable({
            "processing": false,
            "serverSide": false,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
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
                'url': brand_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function(row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('data-brand_id', data.uuid);
                self.set_values(uuid, data.uuid);
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "Name", "data": "name"},
                {"title": "Discount", "data": ""},
                {"title": "Authorized", "data": ""},
                {"title": "Active", "data": ""},
                {"title": "Save", "data": ""},
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
                        return `<input type="number" name="discount" id="discount_${row.uuid}" min="0" value="0">`;
                    }
                },
                {
                    targets: 3,
                    render: function (data, type, row, meta) {
                        return `<input type="checkbox" name="is_authorized" id="is_authorized_${row.uuid}">`;
                    }
                },
                {
                    targets: 4,
                    render: function (data, type, row, meta) {
                        return `<input type="checkbox" name="is_active" id="is_active_${row.uuid}" checked>`;
                    }
                },
                {
                    targets: 5,
                    render: function (data, type, row, meta) {
                        return `<i class="fas fa-save" style="color: #4e73df" id="${row.uuid}"></i>`;
                    }
                },
            ],
        });
    };

    /*
    * =========================================================================
    *                       User edit form setup
    * =========================================================================
    **/

    set_values = (dealer_uuid, brand_uuid) => {
        // add dealer value to each row
        $.ajax({
            url: dealer_brand_api_url + `?brand=${brand_uuid}&dealer=${dealer_uuid}`,
            type: "get",
            success: function (response) {
                if (response.data.length) {
                    let data = response.data[0];
                    $(`#discount_${brand_uuid}`).val(data.discount);
                    (data.is_authorized === true) ?
                        $(`#is_authorized_${brand_uuid}`).prop('checked', true) : '';
                    (data.is_active === true) ? '' :
                        $(`#is_active_${brand_uuid}`).prop('checked', true);
                }
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
    };

    /*
    * =========================================================================
    *                       Dealer Brand Update
    * =========================================================================
    **/

    update = () => {
        // edit user
        $(document).on('click', '.fa-save', function (e) {
            // e.preventDefault();
            let brand_id = $(this).parent().parent().data('brand_id');
            let discount = $(`#discount_${brand_id}`).val();
            let is_authorized = ($(`#is_authorized_${brand_id}`).is(':checked') === true) ? 1 : 0;
            let is_active = ($(`#is_active_${brand_id}`).is(':checked') === true) ? 1 : 0;

            let data = {
                dealer: uuid,
                brand: brand_id,
                discount: discount,
                is_authorized: is_authorized,
                is_active: is_active,
            };

            // submit an ajax request to the api endpoint
            $.ajax({
                url: dealer_brand_api_url,
                type: "POST",
                data: data,
                success: function (resp) {
                    notify('Update successful', 'success')
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
        this.available_brand_list();
        this.update();
    }
}


new Dealer().main();
