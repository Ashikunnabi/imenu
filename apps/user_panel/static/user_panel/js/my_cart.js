/*
* =============================================================================
*                                   MY cart
* =============================================================================
**/

class MyCart {
    cart_data = [];

    toggle_sidebar = () => {
        $("#menu-toggle").click(function (e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
        });

    };

    select_sidebar = () => {
        $("#my_cart").addClass("active");
        let content_height = $(".container-fluid").height();
        // set sidebar height
        $('#sidebar-wrapper').css('height', content_height + 'px');
    };
    /*
    * =========================================================================
    *                       User edit form setup
    * =========================================================================
    **/

    add_cart_list = () => {
        // edit user form value setup
        let self = this;
        $.ajax({
            url: cart_api_url,
            type: "get",
            success: function (response) {
                if (response.data.length < 1){
                    $('#empty_cart').show();
                    $('.cart-view-table').hide();
                    return;
                }
                let total_price = 0;
                self.cart_data = response.data;
                $.each(response.data, function (key, value) {
                    let image_url = value.product_json.image ? '/media/' + value.product_json.image :
                        value.product_json.image_url ? value.product_json.image_url :'/static/base/img/no_image.png';
                    let cart = `                    
                        <tr>
                            <td><a class="remove_cart" data-id="${value.uuid}"><fa class="fa fa-close"></fa></a></td>
                            <td><a href="/product-details/${value.product_json.uuid}/"><img src="${image_url}" alt="img" width="50" height="50"></a></td>
                            <td><a class="aa-cart-title" href="/product-details/${value.product_json.uuid}/">${value.product_json.part_no}</a></td>
                            <td>$${parseFloat(value.unit_price).toFixed(2)}</td>
                            <td>
                                <input class="aa-cart-quantity" type="number" min="0" value="${value.quantity}" data-id="${value.uuid}">
                                <label class="aa-cart-quantity-label" style="color: red"></label>
                            </td>
                            <td>$${parseFloat(value.total_price).toFixed(2)}</td>
                      </tr>
                    `;
                    $('#cart_items').append(cart);
                    total_price += parseFloat(value.total_price);
                });
                $('#subtotal').text('$'+total_price.toFixed(2));
                $('#total').text('$'+total_price.toFixed(2));
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
                        $('#empty_cart').show();
                        $('.cart-view-table').hide();
                        return;
                    }
                }
            }
        });
    };

    update_cart = () => {
        // update a cart from cart list
        let self = this;
        $(document).on('change', '.aa-cart-quantity', function (e) {
            let uuid = $(this).data('id');
            let cart = {};
            $.map(self.cart_data, function (v, i) {
                if (v.uuid === uuid) {
                    cart = v;
                }
            });
            let total_price_text =  $(this).parent().parent().find('td:last-child');
            let input_label = $(this).parent().find('.aa-cart-quantity-label');
            let unit_price = parseFloat(cart.unit_price).toFixed(2);
            let quantity = parseInt($(this).val());
            let discount = parseFloat(cart.discount).toFixed(2);

            // set new total price
            let new_total_price = ((unit_price * quantity) - ((unit_price * quantity) * (discount /100))).toFixed(2);
            $(total_price_text).text('$'+new_total_price);


            // set subtotal and total
            let total = 0;
            $('#cart_items tr').each(function () {
                let item_total =$(this).find('td:last-child').text().replace('$', '');
                total +=  parseFloat(item_total);
            });
            $('#subtotal').text('$'+total.toFixed(2));
            $('#total').text('$'+total.toFixed(2));


            $(input_label).text('Please wait updating changes').css('color', 'red');

            // update db
            let data = {
                quantity: quantity
            };
            $.ajax({
                url: cart_api_url + uuid + '/',
                type: "PATCH",
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (response) {
                    $(input_label).text('Successfully updated').css('color', 'green');
                },
                error: function (response) {
                    $(input_label).text(response.responseJSON.detail).css('color', 'red');
                    setTimeout(function (e) {
                        window.location.reload();
                    }, 800);
                }
            });
        });
    };

    delete_cart = () => {
        // delete a cart from cart list
        $(document).on('click', '.remove_cart', function (e) {
            let self = this;
            let uuid = $(self).data('id');
            $(self).text('PROCESSING');
            $.ajax({
                url: cart_api_url + uuid + '/',
                type: "DELETE",
                success: function (response) {
                    $(self).text('DELETED').css('color', 'red');
                    $(self).parent().parent().css('background-color', 'bisque');
                    setTimeout(function (e) {
                        window.location.reload();
                    }, 800);
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

    place_order = () => {
        $('#place_order_btn').on('click', function (e) {
            e.preventDefault();
            if($('#delivery_address_section:visible').length === 0) {
                // show delivery section
                $('html, body').animate({
                    scrollTop: $("#delivery_address_section").offset().top
                }, 1000);
                $('#delivery_address_section').show('fade').css('display', 'flex');
                $('#place_order_btn').text('Place Order').css('color', 'white');
            } else {
                let shipping_address_form = $('#shipping_address_form');
                let billing_address_form = $('#billing_address_form');
                let shipping_address_form_parsley = shipping_address_form.parsley();
                let billing_address_form_parsley = billing_address_form.parsley();

                if (!shipping_address_form_parsley.isValid()) {
                    shipping_address_form.submit();
                    console.log('invalid shipping');
                    return;
                } else if (!billing_address_form_parsley.isValid()) {
                    billing_address_form.submit();
                    console.log('invalid billing');
                    return;
                } else {
                    if ($('#place_order_payment_button:visible').length === 0) {
                        $('#place_order_payment_button').click().show();
                        $('#place_order_btn').hide();
                        return;
                    }
                }

                $.blockUI({message: '<h1>Please wait, processing payment...</h1>'});
                $('#place_order_btn').text('Processing...');
                let data = {
                    shipping_info: {
                        'full_name': $('#shipping_full_name').val(),
                        'delivery_address': $('#delivery_address').val(),
                        'city': $('#shipping_city').val(),
                        'state': {
                            'value': $('#shipping_state').val(),
                            'text': $('#shipping_state option:selected').text()
                        },
                        'postal_code': $('#shipping_postal_code').val(),
                        'phone': $('#shipping_phone').val(),
                        'email': $('#shipping_email').val(),
                    },
                    billing_info: {
                        'po_number': $('#billing_po_number').val(),
                        'full_name': $('#billing_full_name').val(),
                        'billing_address': $('#billing_billing_address').val(),
                        'city': $('#billing_city').val(),
                        'state': {
                            'value': $('#billing_state').val(),
                            'text': $('#billing_state option:selected').text()
                        },
                        'postal_code': $('#billing_postal_code').val(),
                        'phone': $('#billing_phone').val(),
                        'email': $('#billing_email').val(),
                    },
                    dataDescriptor: $('#dataDescriptor').val(),
                    dataValue: $('#dataValue').val(),
                };
                $.ajax({
                    url: order_api_url,
                    type: "POST",
                    data: JSON.stringify(data),
                    dataType: 'json',
                    contentType: "application/json",
                    success: function (resp) {
                        $.unblockUI();
                        alert('Payment Successful');
                        $('#place_order_btn').text('Order Successful');
                        $('#place_order_btn').off('click');
                        setTimeout(function (e) {
                            window.location.reload();
                        }, 1000);
                    },
                    error: function (response) {
                        $.unblockUI();
                        alert('Failed! Try again');
                        let data = response.responseJSON.detail;
                        $('#place_order_btn').text('Failed!');
                        $('#place_order_btn').off('click');
                        setTimeout(function (e) {
                            window.location.reload();
                        }, 800);
                        console.log(data)
                    }
                });
            }
        });
    };

    copy_shipping_form_data_to_billing_form = () => {
        let shipping = 'shipping';
        let billing = 'billing';

        $('#copy_shipping_data_to_billing').on('click', function (e) {
            $(`#${billing}_full_name`).val($(`#${shipping}_full_name`).val());
            $(`#${billing}_billing_address`).val($(`#delivery_address`).val());
            $(`#${billing}_city`).val($(`#${shipping}_city`).val());
            $(`#${billing}_state`).val($(`#${shipping}_state`).val());
            $(`#${billing}_postal_code`).val($(`#${shipping}_postal_code`).val());
            $(`#${billing}_phone`).val($(`#${shipping}_phone`).val());
            $(`#${billing}_email`).val($(`#${shipping}_email`).val());
        });
    };

    shipping_billing_address_suggestion = () => {
        // shipping address suggestion
        $.ajax({
            url: order_api_url + 'get_user_used_address/?shipping=1',
            type: "GET",
            success: function (response) {
                if (response.data.length) {
                    $('#previously_used_shipping_address').show();
                    $.map(response.data, function (v, i) {
                        let state = null;
                        try {
                            state = JSON.parse(v.state).value;
                        } catch {}

                        $('#shipping_address_suggestion').append(
                            `<option                               
                                data-shipping_full_name="${v.full_name}"
                                data-delivery_address="${v.address}"
                                data-shipping_city="${v.city}"
                                data-shipping_state="${state}"
                                data-shipping_postal_code="${v.postal_code}"
                                data-shipping_phone="${v.phone}"
                                data-shipping_email="${v.email}"
                             >${v.full_name}</option>`
                        )
                    });
                }

                // set shipping form data
                $('#shipping_address_suggestion').on('change', function (e) {
                    $(`#shipping_full_name`).val($(this).children('option:selected').data('shipping_full_name'));
                    $(`#delivery_address`).val($(this).children('option:selected').data('delivery_address'));
                    $(`#shipping_city`).val($(this).children('option:selected').data('shipping_city'));
                    $(`#shipping_state`).val($(this).children('option:selected').data('shipping_state'));
                    $(`#shipping_postal_code`).val($(this).children('option:selected').data('shipping_postal_code'));
                    $(`#shipping_phone`).val($(this).children('option:selected').data('shipping_phone'));
                    $(`#shipping_email`).val($(this).children('option:selected').data('shipping_email'));
                });
            },
            error: function (response) {
                console.log(response)
            }
        });

        // billing address suggestion
        $.ajax({
            url: order_api_url + 'get_user_used_address/?shipping=0',
            type: "GET",
            success: function (response) {
                if (response.data.length) {
                    $('#previously_used_billing_address').show();
                    $.map(response.data, function (v, i) {
                        let state = null;
                        try {
                            state = JSON.parse(v.state).value;
                        } catch {}
                        $('#billing_address_suggestion').append(
                            `<option                               
                                data-billing_full_name="${v.full_name}"
                                data-billing_address="${v.address}"
                                data-billing_city="${v.city}"
                                data-billing_state="${state}"
                                data-billing_postal_code="${v.postal_code}"
                                data-billing_phone="${v.phone}"
                                data-billing_email="${v.email}"
                             >${v.full_name}</option>`
                        )
                    });
                }

                // set billing form data
                $('#billing_address_suggestion').on('change', function (e) {
                    $(`#billing_full_name`).val($(this).children('option:selected').data('billing_full_name'));
                    $(`#billing_billing_address`).val($(this).children('option:selected').data('billing_address'));
                    $(`#billing_city`).val($(this).children('option:selected').data('billing_city'));
                    $(`#billing_state`).val($(this).children('option:selected').data('billing_state'));
                    $(`#billing_postal_code`).val($(this).children('option:selected').data('billing_postal_code'));
                    $(`#billing_phone`).val($(this).children('option:selected').data('billing_phone'));
                    $(`#billing_email`).val($(this).children('option:selected').data('billing_email'));
                });
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    /*
    * =========================================================================
    *                       User edit
    * =========================================================================
    **/

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.toggle_sidebar();
        this.select_sidebar();
        this.add_cart_list();
        this.update_cart();
        this.delete_cart();
        this.place_order();
        this.copy_shipping_form_data_to_billing_form();
        this.shipping_billing_address_suggestion();
    }
}


new MyCart().main();
