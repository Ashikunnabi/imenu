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
                    <h6 class="current-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>${item.prices[0]} Tk+</h6>
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
                <a class="btn btn-sm btn-block btn-outline-primary item-bookmark ${item.uuid}" data-uuid="${item.uuid}" data-json=${JSON.stringify(item)}>SELECT</a>
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
            $(document).find(`.${uuid}`).text("Selected")
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
        let key = "selected_items"
        let selected_items = getLocalWithExpiry(key) || []
        let parent_component = `menu_product_list`

        $.map(selected_items, function (v, i) {
            $.ajax({
                url: `/api/v1/inventory/products/${v}/`,
                method: "GET",
                dataType: "json",
                success: function (data) {
                    $(document).find(`.${parent_component}`).append(
                        productListItemHTML(data.data)
                    )
                    $(document).find(`.${parent_component}`).append(
                        "<br>"
                    )
                    toggleSelectedItem(data.data.uuid);
                },
                error: function (xhr, status, error) {
                    // Handle errors here
                    console.error("AJAX request failed:", status, error);
                }
            });
        })

    }

    // Public methods
    return {
        getProducts: getProducts,
        getSelectedItems: getSelectedItems,
    };
})();
