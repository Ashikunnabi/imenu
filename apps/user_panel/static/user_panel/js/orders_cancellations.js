/*
* =============================================================================
*                                   MY ORDERS CANCELLATIONS
* =============================================================================
**/

class OrdersCancellations {
    orders_cancellations_data = [];

    toggle_sidebar = () => {
        $("#menu-toggle").click(function (e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
        });

    };

    select_sidebar = () => {
        $("#orders_cancellations").addClass("active");
        setInterval(function (e) {
            let content_height = $(".container-fluid").height();
            // set sidebar height
            $('#sidebar-wrapper').css('height', content_height + 'px');
        }, 2000)

    };

    /*
    * =========================================================================
    *                       Order list
    * =========================================================================
    **/

    orders_list = () => {
        let self = this;
        $.ajax({
            url: order_api_url,
            type: "GET",
            success: function (response) {
                if (response.data.length < 1){
                    $('#empty_orders').show();
                    $('.order-view-table').hide();
                    return;
                }
                self.orders_cancellations_data = response.data;
                $.each(response.data, function (key, value) {
                    let status = value.is_delivered ? 'Delivered' : value.in_processing ? 'Processing' : 'Pending';
                    let cancel_option = status === 'Pending' ? `<small data-id=${value.uuid} class="cancel_order">Cancel Order!</small>` : '';
                    let tracking_number = value.tracking_number !== null ? value.tracking_number : '';
                    let show_tracking_number = value.is_delivered ? `<small><strong>Tracking Number:</strong>${tracking_number}</small>` :
                        value.in_processing ? `<small><strong>Tracking Number:</strong>${tracking_number}</small>` : '';
                    let orders_cancellations = `
                        <tr>
                            <td>${key+1}</td>
                            <td class="order_date_time">
                                <span class="day">${moment(value.created_at).format('dddd')}</span>
                                <span class="date">${moment(value.created_at).format('Do')}</span>
                                <span class="month_year">${moment(value.created_at).format('MMM, YYYY')}</span>
                                <span class="time">at ${moment(value.created_at).format('h:mm:ss a')}</span>                                    
                            </td>
                            <td><a class="aa-orders_cancellations-title" href="#"
                                    data-toggle2="tooltip"                       
                                    data-placement="top"                       
                                    title="Order details of 140${value.id}"                       
                                    data-toggle="modal"                      
                                    data-target=".order_details_modal_${value.uuid}"
                                 >140${value.id}</a><br>
                                 ${show_tracking_number}                                 
                            </td>
                            <td>${status} <br> ${cancel_option}</td>
                            <td><a href="/media/${value.invoice}" target="_blank">Download</a></td>
                        </tr>
                    `;
                    $('#orders').append(orders_cancellations);

                    let order_details_modal = `                    
                        <div class="modal fade order_details_modal_${value.uuid}"
                             id="quick-view-modal"
                             tabindex="-1"
                             role="dialog"
                             aria-labelledby="myModalLabel"
                             aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-body">
                                        <button type="button" class="close"
                                                data-dismiss="modal"
                                                aria-hidden="true">&times;
                                        </button>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="cart-view-area">
                                                    <div class="cart-view-table">
                                                        <span class="order_id">Order ID: 140${value.id}</span>
                                                        <span class="order_at">${moment(value.created_at).format('LLLL')}</span>
                                                        <br><br>
                                                        <span><strong>Status:</strong> ${status}</span><br>
                                                        <span class="delivery_address"><strong>Delivery Address:</strong> ${value.delivery_address}</span>
                                                        <hr>
                                                        <div class="table-responsive">
                                                            <table class="table">
                                                                <thead>
                                                                <tr>
                                                                    <th></th>
                                                                    <th>Part Number</th>
                                                                    <th>Price</th>
                                                                    <th>Quantity</th>
                                                                    <th>Total</th>
                                                                </tr>
                                                                </thead>
                                                                <tbody>                                                    
                                                                </tbody>
                                                                <tfoot>
                                                                <tr>
                                                                    <td colspan="3"></td>
                                                                    <td>Subtotal</td>
                                                                    <td>$${value.total_price}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td colspan="3"></td>
                                                                    <td>Total</td>
                                                                    <td>$${value.total_price}</td>
                                                                </tr>
                                                                </tfoot>
                                                            </table>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div><!-- /.modal-content -->
                            </div><!-- /.modal-dialog -->            
                        </div>
                    `;
                    $('#order_details_modals').append(order_details_modal);

                    $.map(value.carts_json, function (v, i) {
                        let image_url = v.product_json.image ? '/media/' + v.product_json.image :
                                        v.product_json.image_url ? v.product_json.image_url :'/static/base/img/no_image.png';
                        let cart_item = `<tr>
                            <td><img src="${image_url}" alt="img" width="50" height="50"></td>
                            <td>${v.product_json.part_no}</td>
                            <td>$${v.unit_price}</td>
                            <td>${v.quantity}</td>
                            <td>$${v.total_price}</td>
                        </tr>`
                        $(`.order_details_modal_${value.uuid} tbody`).append(cart_item)
                    });

                });
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
                    if (response.data.length < 1){
                        $('#empty_orders_cancellations').show();
                        $('.orders_cancellations-view-table').hide();
                        return;
                    }
                }
            }
        });
    };

    /*
    * =========================================================================
    *                       Cancellations list
    * =========================================================================
    **/

    cancellations_list = () => {
        let self = this;
        $.ajax({
            url: order_api_url + '?cancellation=1',
            type: "GET",
            success: function (response) {
                if (response.data.length < 1){
                    $('#empty_orders').show();
                    $('.order-view-table').hide();
                    return;
                }
                self.orders_cancellations_data = response.data;
                $.each(response.data, function (key, value) {
                    let status = 'Cancelled';
                    let orders_cancellations = `
                        <tr>
                            <td>${key+1}</td>
                            <td class="order_date_time">
                                <span class="day">${moment(value.created_at).format('dddd')}</span>
                                <span class="date">${moment(value.created_at).format('Do')}</span>
                                <span class="month_year">${moment(value.created_at).format('MMM, YYYY')}</span>
                                <span class="time">at ${moment(value.created_at).format('h:mm:ss a')}</span>                                    
                                </td>
                            
                            <td><a class="aa-orders_cancellations-title" href="#"
                                    data-toggle2="tooltip"                       
                                    data-placement="top"                       
                                    title="Order details of 140${value.id}"                       
                                    data-toggle="modal"                      
                                    data-target=".order_details_modal_${value.uuid}"
                                 >140${value.id}</a>
                            </td>
                            <td>${status}</td>
                            <td><label class="aa-orders_cancellations-quantity-label" style="color: red"></label></td>
                        </tr>
                    `;
                    $('#orders').append(orders_cancellations);

                    let order_details_modal = `                    
                        <div class="modal fade order_details_modal_${value.uuid}"
                             id="quick-view-modal"
                             tabindex="-1"
                             role="dialog"
                             aria-labelledby="myModalLabel"
                             aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-body">
                                        <button type="button" class="close"
                                                data-dismiss="modal"
                                                aria-hidden="true">&times;
                                        </button>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="cart-view-area">
                                                    <div class="cart-view-table">
                                                        <span class="order_id">Order ID: 140${value.id}</span>
                                                        <span class="order_at">${moment(value.created_at).format('LLLL')}</span>
                                                        <br><br>
                                                        <span><strong>Status:</strong> ${status}</span><br>
                                                        <span class="delivery_address"><strong>Delivery Address:</strong> ${value.delivery_address}</span>
                                                        <hr>
                                                        <div class="table-responsive">
                                                            <table class="table">
                                                                <thead>
                                                                <tr>
                                                                    <th></th>
                                                                    <th>Part Number</th>
                                                                    <th>Price</th>
                                                                    <th>Quantity</th>
                                                                    <th>Total</th>
                                                                </tr>
                                                                </thead>
                                                                <tbody>                                                    
                                                                </tbody>
                                                                <tfoot>
                                                                <tr>
                                                                    <td colspan="3"></td>
                                                                    <td>Subtotal</td>
                                                                    <td>$${value.total_price}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td colspan="3"></td>
                                                                    <td>Total</td>
                                                                    <td>$${value.total_price}</td>
                                                                </tr>
                                                                </tfoot>
                                                            </table>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div><!-- /.modal-content -->
                            </div><!-- /.modal-dialog -->            
                        </div>
                    `;
                    $('#order_details_modals').append(order_details_modal);

                    $.map(value.carts_json, function (v, i) {
                        let image_url = v.product_json.image ? '/media/' + v.product_json.image :
                                        v.product_json.image_url ? v.product_json.image_url :'/static/base/img/no_image.png';
                        let cart_item = `<tr>
                            <td><img src="${image_url}" alt="img" width="50" height="50"></td>
                            <td>${v.product_json.part_no}</td>
                            <td>$${v.unit_price}</td>
                            <td>${v.quantity}</td>
                            <td>$${v.total_price}</td>
                        </tr>`;
                        $(`.order_details_modal_${value.uuid} tbody`).append(cart_item)
                    });
                });
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
                    if (response.data.length < 1){
                        $('#empty_orders_cancellations').show();
                        $('.orders_cancellations-view-table').hide();
                        return;
                    }
                }
            }
        });
    };

    /*
    * =========================================================================
    *                       Cancel Order
    * =========================================================================
    **/

    cancel_order = () => {
        let self = this;

        $(document).on('click', '.cancel_order', function (e) {
           $(this).html(`
                <span>Sure? <a class="yes">YES</a> | <a class="no">NO</a></span>
            `)
        });

        $(document).on('click', '.yes', function (e) {
            console.log('yes')
            let uuid = $(this).parent().parent().data('id');
            let data = {
                'is_cancelled': true
            };
            $.ajax({
                url: order_api_url + `${uuid}/`,
                type: "PATCH",
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (response) {
                    window.location.reload();//
                },
                error: function (response) {
                    console.log(response);
                    window.location.reload();
                }
            });
        });
        $(document).on('click', '.no', function (e) {
            window.location.reload();
        });
    };

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        let self = this;
        self.toggle_sidebar();
        self.select_sidebar();
        self.orders_list();
        $('#toggle_orders_cancellations').on('change', function (e) {
            $('#orders').empty();
            $('.order-view-table').show();
            $('#empty_orders').hide();
            if ($('#toggle_orders_cancellations:checked').length === 1) {
                self.cancellations_list();
            } else {
                self.orders_list();
            }
        });
        self.cancel_order();
    }
}


new OrdersCancellations().main();
