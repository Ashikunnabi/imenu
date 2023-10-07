// Module 1: menuModule.js
export const menuModule = (function () {
    // Private variables and functions

    function menuHTML(menu) {
        let menu__item_class_name = `menu_${menu.uuid}_item-bx`;
        let items = getMenuItems(menu.uuid)

        let html = `
            <div class="title-bar">
                <span class="title mb-0">${menu.name}</span>
            </div>
            <div class="${menu__item_class_name}"></div>
        `
        return html
    }

    function menuItemHTML(item) {
        let document = item.documents ? item.documents[0] : "/static/front_end/assets/images/product/2.jpg"

        let html = `
            <div class="swiper-btn-center-lr mt-0">
                <div class="swiper product-swiper">
                    <div class="swiper-wrapper">
                        <div class="swiper-slide">
                            <div class="card-item style-6">
                                <a href="/product-detail/${item.uuid}/" class="dz-media">
                                    <img src="${document}" alt="image">
                                </a>
                                <div class="dz-content">
                                    <!-- <span class="product-title">Combo pack</span> -->
                                    <h4 class="item-name">
                                        <a href="/product-detail/${item.uuid}/">
                                            ${item.name}
                                        </a>
                                    </h4>
                                    <!-- <div class="offer-code">
                                        FLAT 40% off Code: 636G8P
                                    </div> -->
                                    <div class="footer-wrapper">
                                        <div class="price-wrapper">
                                            <h6 class="current-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>${item.prices[0]} Tk</h6>
                                            <!-- <span class="old-price"><i class="fa-solid fa-bangladeshi-taka-sign"></i>1000</span> -->
                                        </div>
                                        <a class="btn btn-sm btn-outline-primary add-to-cart" data-json=${JSON.stringify(item)}>ADD</a>
                                    </div>
                                    <div class="offer-code">
                                        VAT & SC excluded
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
        return html
    }

    function getMenus() {
        $.ajax({
            url: "/api/v1/menus/",
            method: "GET",
            dataType: "json",
            success: function (data) {
                // Handle the successful response here
                let parent_component = "menus-bx"
                $.map(data.data, function (v, i) {
                    $(document).find(`.${parent_component}`).append(
                        menuHTML(v)
                    )
                })
            },
            error: function (xhr, status, error) {
                // Handle errors here
                console.error("AJAX request failed:", status, error);
            }
        });

    }

    function getMenuItems(menu_uuid) {
        $.ajax({
            url: `/api/v1/menus/${menu_uuid}/items/`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                // Handle the successful response here
                let parent_component = `menu_${menu_uuid}_item-bx`
                $.map(data.data, function (v, i) {
                    $(document).find(`.${parent_component}`).append(
                        menuItemHTML(v)
                    )
                })
            },
            error: function (xhr, status, error) {
                // Handle errors here
                console.error("AJAX request failed:", status, error);
            }
        });

    }

    // Public methods
    return {
        getMenus: getMenus,
    };
})();
