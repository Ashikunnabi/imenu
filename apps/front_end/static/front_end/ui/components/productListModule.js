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
                <a class="btn btn-sm btn-block btn-outline-danger">Clear Cart</a>
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
            <div class="text-end">
                <a href="/product-detail/${item.product.uuid}/" class="dz-media media-100">
                    <img class="rounded-sm" src="${document}" alt="image">
                </a>
            </div>	
        </div>
        `
        return html
    }

    function orderSummaryHTML(order) {

        let html = `
        <div class="product-list">
            <div class="dz-content">
                <span class="product-title">Recent Order</span>
                <h4 class="item-name">
                    <a href="/product-detail//">
                    </a>
                </h4>
                <div class="order_summary_order_list">                   
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

    function getSelectedItems() {
        let cart = new Cart().get()
        let parent_component = `menu_product_list`

        $.map(cart.lines, function (v, i) {

            $(document).find(`.${parent_component}`).append(
                cartListItemHTML(v)
            )
            $(document).find(`.${parent_component}`).append(
                "<br>"
            )
            toggleSelectedItem(v.product.uuid);
        })

        $(document).find(`.${parent_component}`).append(
            cartSummaryHTML(cart)
        )


        // order section
        let order = new Order().get()
        let order_summary_order_list = "order_summary_order_list"

        $(document).find(`.${parent_component}`).append(
            "<br><hr><br>"
        )
        $(document).find(`.${parent_component}`).append(
            orderSummaryHTML(order)
        )

        $.map(order.lines, function (v, i) {
            $(document).find(`.${order_summary_order_list}`).append(
                orderListItemHTML(v)
            )
            $(document).find(`.${order_summary_order_list}`).append(
                "<br>"
            )
        })
        

    }

    // Public methods
    return {
        getProducts: getProducts,
        getSelectedItems: getSelectedItems,
    };
})();
