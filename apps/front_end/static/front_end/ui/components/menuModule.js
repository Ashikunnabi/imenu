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
            <div class="swiper-btn-center-lr mt-0">
                <div class="swiper product-swiper">
                    <div class="swiper-wrapper ${menu__item_class_name}">
                        <!-- <div class="${menu__item_class_name}"></div> -->
                    </div>
                </div>
            </div>
        `
        return html
    }

    function menuItemHTML(item) {
        let document = item.documents ? item.documents[0] : "/static/front_end/assets/images/product/2.jpg"

        let html = `
            <div class="swiper-slide">
                <div class="card-item style-6">
                    <a href="/product-detail/${item.uuid}/" class="dz-media">
                        <img src="${document}" alt="image">
                    </a>
                    <div class="dz-content">
                        <span class="product-title">${item.code}</span>
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
                            <a class="btn btn-sm btn-outline-primary add-to-cart item-bookmark ${item.uuid}" data-uuid="${item.uuid}" data-json=${JSON.stringify(item)}>SELECT</a>
                        </div>
                        <div class="offer-code">
                            VAT & SC excluded
                        </div>
                    </div>
                </div>
            </div>
        `
        return html
    }

    function getMenus() {
        $.ajax({
            url: "/api/v1/menus/?is_pinned=0",
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

    function initiateProductSlider(container_class) {
        if (jQuery(`.${container_class}`).length > 0) {
            var swiperRecomandSwiper = new Swiper('.product-swiper', {
                speed: 500,
                parallax: true,
                slidesPerView: 'auto',
                spaceBetween: 0,
                loop: false,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },
            });
        }
    }

    function toggleSelectedItem(uuid) {
        let key = "selected_items"
        let selected_items = getLocalWithExpiry(key) || []

        if (selected_items.includes(uuid)) {
            $(document).find(`.${uuid}`).addClass("active")
            $(document).find(`.${uuid}`).text("Selected")
        }
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
                    toggleSelectedItem(v.uuid)
                })
                initiateProductSlider("product-swiper")
            },
            error: function (xhr, status, error) {
                // Handle errors here
                console.error("AJAX request failed:", status, error);
            }
        });
    }

    function getSearchItems() {
        let parent_search_result_class_name = "search-result-bx"
        let search_result_title_class_name = "search-result-title"
        let search_result_class_name = "search-result-items"
        $(document).find(`.${parent_search_result_class_name}`).hide()

        $(document).on('change paste keyup', '.search-input,.form-control', function () {
            $(document).find(`.${parent_search_result_class_name}`).show()

            if ($(this).val().length > 0) {
                let search_text = $(this).val()

                $.ajax({
                    url: `/api/v1/menus/search/items/?is_pinned=0&search=${search_text}`,
                    method: "GET",
                    dataType: "json",
                    success: function (data) {
                        // Handle the successful response here
                        $(document).find(`.${search_result_class_name}`).html("")
                        $(document).find(`.${search_result_title_class_name}`).html(`We found ${data.data.length} results for "${search_text}"`)

                        $.map(data.data, function (v, i) {
                            $(document).find(`.${search_result_class_name}`).append(
                                menuItemHTML(v)
                            )
                            toggleSelectedItem(v.uuid)
                        })

                        if (data.data.length < 1) {
                            $(document).find(`.${search_result_title_class_name}`).html(`Sorry, we found ${data.data.length} results for "${search_text}"`)
                            $(document).find(`.${search_result_class_name}`).html("<span style='margin: 0 auto'>No results found</span>")
                        } else {
                            initiateProductSlider("product-swiper")
                        }
                    },
                    error: function (xhr, status, error) {
                        // Handle errors here
                        console.error("AJAX request failed:", status, error);
                        $(document).find(`.${search_result_class_name}`).html("<span style='margin: 0 auto'>No results found</span>")
                    }
                });
            } else {
                $(document).find(`.${parent_search_result_class_name}`).hide()
            }
        })
    }

    // Public methods
    return {
        getMenus: getMenus,
        getSearchItems: getSearchItems,
    };
})();
