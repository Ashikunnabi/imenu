/*
* =============================================================================
*                                   ORDER
* =============================================================================
**/

class Order {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_order_management_a').click();
        $('#sidebar_option_order_management_order').addClass('active');
    };

    /*
    * =========================================================================
    *                       Order in Datatable
    * =========================================================================
    **/
    list = (q=null) => {
        let self = this;
        let table = $('#orderDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B><"extra_btn">flrtip',
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
                'url': order_api_url,
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
                {"title": "Status", "data": "status"},
                {"title": "Order ID", "data": ""},
                {"title": "Table", "data": "table.name"},
                {"title": "total_price_ex_vat", "data": "total_price_ex_vat"},
                {"title": "total_price_in_vat", "data": "total_price_in_vat"},
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
                        return '140' + row.id;
                    }
                },
                // {
                //     targets: 2,
                //     render: function (data, type, row, meta) {
                //         return row.user_json.name;
                //     }
                // },
                // {
                //     targets: 3,
                //     render: function (data, type, row, meta) {
                //         return row.user_json.phone;
                //     }
                // },
            ],
        });

        // add extra inputs for additional filtering
        $("div.extra_btn").html(`
            <div class="row">
                <div class="col-md-12">
                
                    <div class="form-group">
                    
                        <div class="custom-control custom-checkbox" style="display: inline-block; margin-left: 5px">
                            <input type="checkbox" class="custom-control-input"
                                   id="pending_extra_btn" name="pending_extra_btn">
                            <label class="custom-control-label"
                                   for="pending_extra_btn">Pending</label>
                        </div>
                    
                        <div class="custom-control custom-checkbox" style="display: inline-block; margin-left: 5px">
                            <input type="checkbox" class="custom-control-input"
                                   id="in_processing_extra_btn" name="in_processing_extra_btn">
                            <label class="custom-control-label"
                                   for="in_processing_extra_btn">In Processing</label>
                        </div>
                        
                        <div class="custom-control custom-checkbox" style="display: inline-block; margin-left: 5px">
                            <input type="checkbox" class="custom-control-input"
                                   id="is_delivered_extra_btn" name="is_delivered_extra_btn">
                            <label class="custom-control-label"
                                   for="is_delivered_extra_btn">Delivered</label>
                        </div>
                        
                        <div class="custom-control custom-checkbox" style="display: inline-block; margin-left: 5px">
                            <input type="checkbox" class="custom-control-input"
                                   id="is_cancelled_extra_btn" name="is_cancelled_extra_btn">
                            <label class="custom-control-label"
                                   for="is_cancelled_extra_btn">Cancelled</label>
                        </div>
                        
                    </div>                    
                </div>
            </div>
        `);

        // additional filter based on extra button
        $('.custom-control-input').on('change', function (e) {
            let url = order_api_url;

            $(`#pending_extra_btn`).prop('checked', false);
            $(`#in_processing_extra_btn`).prop('checked', false);
            $(`#is_delivered_extra_btn`).prop('checked', false);
            $(`#is_cancelled_extra_btn`).prop('checked', false);
            $(`#${$(this).attr('id')}`).prop('checked', true);

            if ($(`#pending_extra_btn`).is(':checked')) {
                url += '?pending=1';
            }

            if ($(`#in_processing_extra_btn`).is(':checked')) {
                url += '?processing=1';
            }

            if ($(`#is_delivered_extra_btn`).is(':checked')) {
                url += '?delivered=1';
            }

            if ($(`#is_cancelled_extra_btn`).is(':checked')) {
                url += '?cancellation=1';
            }
            table.ajax.url( url ).load();
        });



        // Single click row select the row and mark a different color
        $('#orderDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#orderDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });

        // initial filter by query parameter
        if (q !== null || q !== '' || q !== undefined) {
            switch (q) {
                case '1':
                    $(`#pending_extra_btn`).click();
                    break;
                case '2':
                    $(`#in_processing_extra_btn`).click();
                    break;
                case '3':
                    $(`#is_delivered_extra_btn`).click();
                    break;
                case '4':
                    $(`#is_cancelled_extra_btn`).click();
                    break;
                default:
                    break;
            }
        }
    };

    /*
    * =========================================================================
    *                       Order details page
    * =========================================================================
    **/
    detail_page_setup = () => {
        let self = this;
        $.ajax({
            url: order_api_url + `${uuid}/`,
            type: "GET",
            success: function (resp) {
                self.order_detail_template(resp.data)
            },
            error: function (response) {
                let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
                        }
            }
        });
    };

    /*
    * =========================================================================
    *                       Order details template
    * =========================================================================
    **/

    order_detail_template = (order) => {
        let order_detail = `
            <div class="row">
                <div class="col-md-12">
                    <div class="cart-view-area">
                        <div class="cart-view-table">
                            <span class="delivery_address"><strong>Status:</strong> ${order.status}</span><br>
                            <span class="order_id"><strong>Order ID:</strong> 140${order.id}</span>
                            <br>
                            <span><strong>Table:</strong> ${order.table.name}</span><br>
                            <span><strong>Ordered At:</strong> ${moment(order.created_at).format('LLLL')}</span><br>
                            <hr>
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                    <tr>
                                        <th>SL</th>
                                        <th>Image</th>
                                        <th>Item</th>
                                        <th>Price</th>
                                        <th>Quantity</th>
                                        <th>Total</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    </tbody>
                                    <tfoot>
                                    <tr>
                                        <td colspan="4"></td>
                                        <td>Subtotal</td>
                                        <td>${order.total_price_ex_vat}</td>
                                    </tr>
                                    <tr>
                                        <td colspan="4"></td>
                                        <td>Total</td>
                                        <td>${order.total_price_in_vat}</td>
                                    </tr>
                                    </tfoot>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        $('#order_detail').append(order_detail);

        $.map(order.lines, function (v, i) {
            let image_url = v.product.documents ? v.product.documents[0] : '/static/base/img/no_image.png';
            let cart_item = `<tr>
                <td>${i+1}</td>
                <td><img src="${image_url}" alt="img" width="50" height="50"></td>
                <td>${v.product.code} - ${v.product.name}</td>
                <td>${v.product.prices[0]}</td>
                <td>${v.quantity}</td>
                <td>${v.total_price_in_vat}</td>
            </tr>`
            $(`#order_detail tbody`).append(cart_item)
        });

        $(`input[name="status"][value="${order.status}"]`).prop('checked', true);
    };

    /*
    * =========================================================================
    *                       Order Update
    * =========================================================================
    **/

    update = () => {
        // edit user
        $(document).on('click', '#submit_changes', function (e) {
            e.preventDefault();
            let status = $('input[name="status"]:checked').val();

            let data = {
                status: status,
            };

            // submit an ajax request to the api endpoint
            $.ajax({
                url: order_api_url + `${uuid}/`,
                type: "PATCH",
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
        let searchParams = new URLSearchParams(window.location.search);
        this.select_sidebar_option();
        if (page === 'list') this.list(searchParams.get('q'));
        if (page === 'edit') this.detail_page_setup();
        if (page === 'edit') this.update();
    }
}


new Order().main();
