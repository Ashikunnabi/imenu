// Module 1: productListModule.js
export const productListModule = (function () {
    // Private variables and functions

    function productListItemHTML(item) {
        let document = item.documents ? item.documents[0] : "/static/front_end/assets/images/product/2.jpg"

        let html = `
        <div class="product-list">
            <div class="dz-content">
                <span class="product-title">${item.code}</span>
                <h4 class="item-name">
                    <a href="/product-detail/${item.uuid}/">
                        ${item.name}
                    </a>
                </h4>
                <div class="price-wrapper">
                    <h6 class="current-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>${item.prices[0]} Tk</h6>
                    <!--<span class="old-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>1100</span>-->
                </div>
                <div class="offer-code">
                    VAT & SC excluded
                </div>
                <!--<div class="footer-wrapper">
                    <span class="product-title">Combo pack</span>
                </div>-->
            </div>
            <div class="text-end">
                <a href="/product-detail/${item.uuid}/" class="dz-media media-100">
                    <img class="rounded-sm" src="${document}" alt="image">
                </a>
                <a class="btn btn-sm btn-block btn-outline-primary item-bookmark ${item.uuid}" data-uuid="${item.uuid}" data-json=${JSON.stringify(item)}>Add</a>
            </div>	
        </div>
        `
        return html
    }

    function cartListItemHTML(item) {
        let document = item.product.documents ? item.product.documents[0] : "/static/front_end/assets/images/product/2.jpg"

        let html = `
        <div class="product-list">
            <div class="dz-content">
                <span class="product-title">${item.product.code}</span>
                <h4 class="item-name">
                    <a href="/product-detail/${item.product.uuid}/">
                        ${item.product.name}
                    </a>
                </h4>
                <div class="price-wrapper">
                    <h6 class="current-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>${item.total_price_ex_vat} Tk</h6>
                    <!--<span class="old-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>1100</span>-->
                </div>
                <div class="offer-code">
                    VAT & SC excluded
                </div>
                <!--<div class="footer-wrapper">
                    <span class="product-title">Combo pack</span>
                </div>-->
            </div>

            <div class="dz-content">
                <div class="dz-stepper border-1 stepper-fill">
                    <br>
                    <!--<small>Fill Stepper</small>-->
                    <input class="stepper cart_item_quantity" type="text" data-uuid="${item.uuid}" value="${item.quantity}" name="demo3">
                </div>
            </div>

            <div class="text-end">
                <a href="/product-detail/${item.product.uuid}/" class="dz-media media-100">
                    <img class="rounded-sm" src="${document}" alt="image">
                </a>
                <a class="btn btn-sm btn-block btn-outline-primary item-bookmark ${item.product.uuid}" data-uuid="${item.product.uuid}" data-json=${JSON.stringify(item)}>Add</a>
            </div>	
        </div>
        `
        return html
    }

    function cartSummaryHTML(cart) {

        let html = `
        <div class="product-list">
            <div class="dz-content">
                <span class="product-title"></span>
                <h4 class="item-name">
                    <a href="/product-detail//">
                    </a>
                </h4>
                <div class="price-wrapper">
                    <h6 class="current-price-"><i class="fa-solid fa-bangladeshi-taka-sign"></i>TOTAL PAYABLE</h6>
                    <!--<span class="old-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>1100</span>-->                    
                </div>
                <div class="offer-code">
                    Enjoy your meal!
                </div>
                <!--<div class="footer-wrapper">
                    <span class="product-title">Combo pack</span>
                </div>-->
            </div>
            <div class="text-end">
                <table>
                    <tr>
                        <td style="padding-right:50px">Subtotal</td>
                        <td style="text-align:left">${cart.total_price_ex_vat} Tk</td>
                    </tr>
                    <tr>
                        <td style="padding-right:50px">Vat</td>
                        <td style="text-align:left">${cart.vat} Tk</td>
                    </tr>
                    <tr>
                        <td style="padding-right:50px"><h5 style="color:#009688;">Total</h5></td>
                        <td style="text-align:left"><h5 style="color:#009688;">${cart.total_price_in_vat} Tk</h5></td>
                    </tr>
                </table>
                <a class="btn btn-sm btn-block btn-outline-primary active btn_place_order">Place Order</a><br>
                <a class="btn btn-sm btn-block btn-outline-danger btn_clear_cart">Clear Cart</a>
            </div>
        </div>
        `
        return html
    }

    function orderListItemHTML(item) {
        let document = item.product.documents ? item.product.documents[0] : "/static/front_end/assets/images/product/2.jpg"

        let html = `
        <div class="product-list" style="padding: 0;background: none;box-shadow: none;margin: 0;">
            <div class="dz-content">
                <span class="product-title">${item.product.code}</span>
                <h4 class="item-name">
                    <a href="/product-detail/${item.product.uuid}/">
                        ${item.product.name}
                    </a>
                </h4>
                <div class="price-wrapper">
                    <h6 class="current-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>${item.total_price_ex_vat} Tk</h6>
                    <!--<span class="old-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>1100</span>-->
                </div>
                <!--<div class="offer-code">
                    VAT & SC excluded
                </div>
                <div class="footer-wrapper">
                    <span class="product-title">Combo pack</span>
                </div>-->
            </div>
            <div class="dz-content">
                <div>
                    <span>${item.price_ex_vat} X ${item.quantity}</span>

                </div>
            </div>
            <div class="text-end">
                <a href="/product-detail/${item.product.uuid}/" class="dz-media media-100">
                    <img class="rounded-sm" src="${document}" alt="image">
                </a>
            </div>	
        </div>
        `
        return html
    }

    function orderStatusText(status) {
        let order_status_messages = {
            "order_placed": "Your culinary journey begins. Order confirmed, let the feast planning commence!",
            "food_preparation": "Chef is turning up the heat, cooking your masterpiece. Get ready for delicious drama!",
            "food_ready": "Your dish is now a superstar, ready to make its debut at your table.",
            "out_for_delivery": "Your order is making a grand entrance! Prepare for the ultimate dining experience.",
            "on_your_table": "Cue the applause! Your food has arrived. It's showtime at your table!",
            "ready_to_indulge": "Time to savor the spotlight. Your meal awaits — enjoy the culinary spectacle!",
            "payment_ready": "Bill's here! It's time to settle up. Enjoy your meal!",
            "payment_done": "Thanks. Your payment has been received. Enjoy your meal!",
            "canceled": "Your order has been cancelled. We hope to see you again soon!",
        }
        return order_status_messages[status]
    }

    function orderSummaryHTML(order) {

        let html = `
        <div class="product-list">
            <div class="dz-content">
                <span class="product-title">Recent Order #00000000${order.id}</span>
                <br>
                <span style="background: #009688;padding: 2px 5px;border-radius: 2em;color: white;margin-top: 7px;">${order.status.replace(/_/g, ' ').toUpperCase()} </span>
                <br>
                <span class="offer-code">${orderStatusText(order.status)} </span>
                <h4 class="item-name">
                    <a href="/product-detail//">
                    </a>
                </h4>
                <div class="order_summary_order_list_${order.uuid}">                   
                </div>

            <div class="text-end">
            <table>
                <tr>
                    <td style="padding-right:50px">Subtotal</td>
                    <td style="text-align:left">${order.total_price_ex_vat} Tk</td>
                </tr>
                <tr>
                    <td style="padding-right:50px">Vat</td>
                    <td style="text-align:left">${order.vat} Tk</td>
                </tr>
                <tr>
                    <td style="padding-right:50px"><h5 style="color:#009688;">Total</h5></td>
                    <td style="text-align:left"><h5 style="color:#009688;">${order.total_price_in_vat} Tk</h5></td>
                </tr>
            </table>
        </div>
                <!--<div class="offer-code">
                    Enjoy your meal!
                </div>-->
                <!--<div class="footer-wrapper">
                    <span class="product-title">Combo pack</span>
                </div>-->
            </div>
        </div>
        `
        return html
    }

    function getMenuUUIDFromURL() {
        // Get the current URL
        var url = window.location.href;

        // Split the URL by '/' to get individual parts
        var urlParts = url.split('/');

        // Find the UUID in the URL
        var uuid = null;
        for (var i = 0; i < urlParts.length; i++) {
            if (/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(urlParts[i])) {
                // Found a UUID-like string
                uuid = urlParts[i];
                break; // Exit the loop once found
            }
        }

        // Check if a UUID was found
        if (uuid == null) {
            console.log("UUID not found in the URL.");
        }
        return uuid
    }


    function toggleSelectedItem(uuid) {
        let key = "selected_items"
        let selected_items = getLocalWithExpiry(key) || []

        if (selected_items.includes(uuid)) {
            $(document).find(`.${uuid}`).addClass("active")
            $(document).find(`.${uuid}`).text("Remove")
        }
    }

    function getProducts() {
        let menu_uuid = getMenuUUIDFromURL()
        $.ajax({
            url: `/api/v1/menus/${menu_uuid}/items/`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                // Handle the successful response here
                let parent_component = `menu_product_list`
                $.map(data.data, function (v, i) {
                    $(document).find(`.${parent_component}`).append(
                        productListItemHTML(v)
                    )
                    toggleSelectedItem(v.uuid);
                })
            },
            error: function (xhr, status, error) {
                // Handle errors here
                console.error("AJAX request failed:", status, error);
            }
        });

    }

    function getCartItems(instance) {
        let cart = instance || new Cart().get()
        let cart_component = `cart_items`

        // make empty
        $(document).find(`.${cart_component}`).html("")

        // cart section
        if (cart) {
            $.map(cart.lines, function (v, i) {

                $(document).find(`.${cart_component}`).append(
                    cartListItemHTML(v)
                )
                $(document).find(`.${cart_component}`).append(
                    "<br>"
                )
                toggleSelectedItem(v.product.uuid);
            })

            $(document).find(`.${cart_component}`).append(
                cartSummaryHTML(cart)
            )
            $(".stepper").TouchSpin();
        }
    }

    function getOrderItems(instances) {
        let orders = instances || new Order().get()
        let orders_component = `orders_items`
        let order_summary_order_list = "order_summary_order_list"

        // make empty
        $(document).find(`.${orders_component}`).html("")

        // order section
        if (orders) {
            $(document).find(`.${orders_component}`).append(
                "<br><hr><br>"
            )
            $.each(orders, function (index, order) {
                $(document).find(`.${orders_component}`).append(
                    orderSummaryHTML(order)
                )

                $.map(order.lines, function (v, i) {
                    $(document).find(`.${order_summary_order_list}_${order.uuid}`).append(
                        orderListItemHTML(v)
                    )
                    $(document).find(`.${order_summary_order_list}_${order.uuid}`).append(
                        "<br>"
                    )
                })
            })
        }
    }


    function getSelectedItems(refresh_cart = false, refresh_order = false) {
        let parent_component = `menu_product_list`
        let cart = new Cart().get()
        let orders = new Order().get()

        if (!cart && !orders.length) {
            // make empty
            $(document).find(`.${parent_component}`).html("").append(
                "<h6>No recent order/cart found.</h6>"
            )
            notify("error", "Please add items to cart first.")
            return
        }

        if (refresh_cart) {
            getCartItems(cart)
        }
        if (refresh_order) {
            getOrderItems(orders)
        }

    }

    function refetchCartOrder(milisecond = 10000) {
        setInterval(function () {
            getSelectedItems(true, true)
        }, milisecond);
    }

    // Public methods
    return {
        getProducts: getProducts,
        getSelectedItems: getSelectedItems,
        refetchCartOrder: refetchCartOrder,
    };
})();
