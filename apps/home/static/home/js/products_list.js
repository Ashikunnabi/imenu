/*
* =============================================================================
*                                   PRODUCT LIST
* =============================================================================
**/

class ProductList {
    sidebar_selected_category_id = null;
    sidebar_selected_brand_id = null;
    text_based_search = '';
    authorization_url = '#';
    /*
    * =========================================================================
    *                       Product List page
    * =========================================================================
    **/
    on_load_filter_product = () => {
        let self = this;

        setTimeout(function (e) {
            const urlParams = new URLSearchParams(window.location.search);
            const category_hashed_id = urlParams.get('category');
            const brand_hashed_id = urlParams.get('brand');
            self.text_based_search = urlParams.get('q');
            self.type = urlParams.get('type')
            self.year = urlParams.get('year')
            self.brand = urlParams.get('adv_brand')
            self.model = urlParams.get('model')

            if (category_hashed_id) {
                $(`#custom_sidebar_category_${category_hashed_id}`).trigger('click');
            }

            if (brand_hashed_id) {
                $(`#custom_sidebar_brand_${brand_hashed_id}`).trigger('click');
            }

            if (self.text_based_search) {
                $('#pagination').twbsPagination('destroy');
                self.product(null, '', self.text_based_search)
            } else {
                self.text_based_search = '';
            }

            if (self.type == '2') {
                self.product(null, '', '', `type=2&year=${self.year}&sidebar_brand=${self.brand}&model=${self.model}`)
            }
        }, 2000);
    };

    banner = () => {
        let self = this;
        $.ajax({
            url: banner_api_url,
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    if (value.human_readable_page === 'Product list page') {
                        $('#aa-catg-head-banner').show();
                        $('#aa-catg-head-banner a').attr('href', value.redirect_url);
                        $('#aa-catg-head-banner a img').attr('src', "/media/"+value.image)
                        // $('.aa-catg-head-banner-area div div h2').html(value.title)
                    }
                })
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    sidebar_category = () => {
        $.ajax({
            url: product_category_api_url,
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (v, i) {
                    $('#sidebar_category').append(`<li><a id="custom_sidebar_category_${v.hashed_id}" href="javascript:;" data-id="${v.hashed_id}">${v.name}</a></li>`);
                });
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    sidebar_brand = (category=null) => {
        let url = category ? brand_api_url + `?category=${category}` : brand_api_url;
        $.ajax({
            url: url,
            type: "GET",
            success: function (resp) {
                $('.tag-cloud').empty();
                $.map(resp.data, function (v, i) {
                    $('.tag-cloud').append(`<a href="javascript:;" id="custom_sidebar_brand_${v.hashed_id}" data-id="${v.hashed_id}">${v.name}</a>`);
                });
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    clear_sidebar_selection = () => {
        let self = this;
        $('#clear_category_selection').on('click', function (e) {
                self.sidebar_selected_category_id = null;
                self.sidebar_selected_brand_id = null;
                $('#sidebar_category li a').removeClass('sidebar_active_product');
                self.sidebar_brand(self.sidebar_selected_category_id);
                $('#pagination').twbsPagination('destroy');
                self.product(null)
        });

        $('#clear_brand_selection').on('click', function (e) {
                self.sidebar_selected_brand_id = null;
                $('.tag-cloud a').removeClass('sidebar_active_brand');
                self.sidebar_brand(self.sidebar_selected_category_id);
                $('#pagination').twbsPagination('destroy');
                self.product(null)
        });
    };

    image_url_generator(product) {
        let url = '/static/base/img/no_image.png';
        url = product.image_url ? product.image_url :
            product.image ? '/media/' + product.image : url
        return url;
    }

    product_template = (product) => {
        let self = this;
        let image_url = self.image_url_generator(product)
        return `  <li>
        <figure>
            <a class="aa-product-img" href="/product-details/${product.hashed_id}">
            <img
                src="${image_url}"
                alt=""
                width="100%" height="300"
            ></a>
            <a class="aa-add-card-btn cart_btn_${product.hashed_id}"
                data-id="${product.hashed_id}" data-quantity="1"
                href="#"><span
                class="fa fa-cart-plus"></span>Add
            To Cart</a>
            <figcaption>
                <h4 class="aa-product-title"><a
                    href="/product-details/${product.hashed_id}">${product.description}</a>
                </h4>
                <!--                        <span class="aa-product-price">$${product.current_price}</span>-->
                <!--                         ${product.previous_price ? '<span class="aa-product-price"><del>$${product.previous_price}</del></span>' : ''}-->
                <!--                        <p class="aa-product-descrip">Lorem-->
                <!--                            ipsum dolor sit amet,-->
                <!--                            consectetur adipisicing elit.-->
                <!--                            Numquam accusamus facere iusto,-->
                <!--                            autem soluta amet sapiente-->
                <!--                            ratione inventore nesciunt a,-->
                <!--                            maxime quasi consectetur, rerum-->
                <!--                            illum.</p>-->
            </figcaption>
        </figure>
        <div class="aa-product-hvr-content">
            <a href="#" data-toggle="tooltip"
                data-placement="top"
                title="Add to Wishlist"><span
                class="fa fa-heart-o"></span></a>
            <!--<a href="#" data-toggle="tooltip" data-placement="top" title="Compare"><span class="fa fa-exchange"></span></a>-->
            <a href="#" data-toggle2="tooltip"
                data-placement="top"
                title="Quick View"
                data-toggle="modal"
                data-target=".quick-view-modal-${product.hashed_id}"><span
                class="fa fa-search"></span></a>
        </div>
        <!-- product badge -->
        <!--<span class="aa-badge aa-sale" href="#">SALE!</span>-->
    </li>
    ` +`
    <div class="modal fade quick-view-modal-${product.hashed_id}" id="quick-view-modal"
        tabindex="-1" role="dialog"
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
                        <!-- Modal view slider -->
                        <div class="col-md-5 col-sm-5 col-xs-12">
                            <div class="aa-product-view-slider">
                                <div id="demo-${product.hashed_id}"
                                    class="simpleLens-gallery-container">
                                    <div class="simpleLens-container">
                                        <div class="simpleLens-big-image-container">
                                            <a data-lens-image="${image_url}"
                                                class="simpleLens-lens-image">
                                            <img src="${image_url}"
                                                class="simpleLens-big-image">
                                            </a>
                                        </div>
                                    </div>
                                    <div class="simpleLens-thumbnails-container">
                                        <a data-big-image="${image_url}"
                                            data-lens-image="${image_url}"
                                            class="simpleLens-thumbnail-wrapper"
                                            href="#">
                                        <img src="${image_url}"
                                            width="45"
                                            height="55">
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Modal view content -->
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="aa-product-view-content">
                                <!-- PART NUMBER -->
                                <h5>
                                    <strong>Part Number: 
                                    <span>${product.part_no}</span>
                                    </strong>
                                </h5>
                                <!-- PRODUCT AVAILABILIY -->
                                <p class="aa-product-avilability">
                                    <span>
                                    <span id="live_stock_${product.hashed_id}"></span>
                                    In stock
                                    </span>
                                </p>
                                <!-- PRODUCT TITLE/DESCRIPTION -->
                                <h4 class="title">${product.description}</h4>
                                <!-- PRODUCT TAGS -->
                                <div class="tag">
                                    <span class="tag1">
                                    <a 
                                        href="/product-list/?brand=${product.manufacturer_hashed_id}" 
                                        target="_blank"
                                        >
                                    ${product.manufacturer_human_readable}
                                    </a>
                                    </span> 
                                    &nbsp;
                                    <span class="tag2">
                                    <a 
                                        href="/product-list/?category=${product.category_hashed_id}" 
                                        target="_blank"
                                        >
                                    ${product.category_human_readable}
                                    </a>
                                    </span>
                                </div>
                                <!-- PRODUCT PRICE -->
                                <h2 class="productPrice">$${product.your_price}</h2>
                                <!-- OTHER PRICES -->
                                <table>
                                    <tr>
                                        <th colspan="3">Price</th>
                                    </tr>
                                    <tr>
                                        <th>JOBBER</th>
                                        <th>MAP</th>
                                        <th>MSRP</th>
                                    </tr>
                                    <tr>
                                        <td>$ ${product.jobbar_price}</td>
                                        <td>$ ${product.map_price}</td>
                                        <td>$ ${product.retail_price}</td>
                                    </tr>
                                </table>
                                <hr/>
                                <!-- SELECT PRODUCT QUANTITY AND WEARHOUSE FOR ORDER -->
                                <div class="aa-prod-quantity">
                                    <span>
                                    <label>Quantity: </label>
                                    <input 
                                        type="number" 
                                        value="1" 
                                        min="0" 
                                        max="0"
                                        id="product_amount_${product.hashed_id}"
                                        data-product_hashed_id="${product.hashed_id}"
                                        >
                                    </span>
                                    <!--<span>
                                        <label>Wearhouse: </label>
                                        <select>
                                            <option>Location 1: 30</opion>
                                            <option>Location 2: 00</opion>
                                            <option>Location 3: 20</opion>
                                            <option>Location 4: 130</opion>
                                            <option>Location 5: 10</opion>
                                        </select>-->
                                    </span>
                                </div>
                            </div>
                            <!-- SPECIAL ORDER IMAGE -->
                            <div class="aa-prod-view-bottom" id="special_order_div_${product.hashed_id}" style="display: none">
                                <img src="/static/base/company/img/special_order.png" style="width: 100%">
                            </div>
                            <!-- UNAUTHORIZED DECLARATION  -->
                            <div class="aa-prod-view-bottom unauthorized_order" id="unauthorized_order_div_${product.hashed_id}">
                                <p class="text-danger">* You are not authorized to purchase this product due to vendor restrictions.</p>
                                <p><a href="${product.authorization_form_url}">Click here!</a> to apply for authorization.</p>
                            </div>
                            <!-- ADD TO CART FOR ORDER WITH WISHLIST -->
                            <div class="aa-prod-view-bottom">
                                <a class="aa-add-to-cart-btn aa-add-card-btn cart_btn_${product.hashed_id}"
                                    data-id="${product.hashed_id}" data-quantity="1"
                                    href="#">Add To Cart</a>
                                <a class="aa-add-to-cart-btn"
                                    href="#">Wishlist</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
        `
    };

    depricated_product_template = (product) => {
        let image_url = product.image_url ? product.image_url :
            product.image ? '/media/' + product.image : '/static/base/img/no_image.png';
        return `          
            <li>
                <figure>
                    <!-- <a class="aa-product-img" href="#"><img src="img/women/girl-1.png" alt="polo shirt img"></a> -->
                    <a class="aa-product-img" href="/product-details/${product.hashed_id}"><img
                            src="${image_url}"
                            alt=""
                            width="100%" height="300"></a>
                    <a class="aa-add-card-btn cart_btn_${product.hashed_id}"
                       data-id="${product.hashed_id}" data-quantity="1"
                       href="#"><span
                            class="fa fa-cart-plus"></span>Add
                        To Cart</a>
                    <figcaption>
                        <h4 class="aa-product-title"><a
                                href="/product-details/${product.hashed_id}">${product.description}</a>
                        </h4>
<!--                        <span class="aa-product-price">$${product.current_price}</span>-->
<!--                         ${product.previous_price ? '<span class="aa-product-price"><del>$${product.previous_price}</del></span>' : ''}-->
<!--                        <p class="aa-product-descrip">Lorem-->
<!--                            ipsum dolor sit amet,-->
<!--                            consectetur adipisicing elit.-->
<!--                            Numquam accusamus facere iusto,-->
<!--                            autem soluta amet sapiente-->
<!--                            ratione inventore nesciunt a,-->
<!--                            maxime quasi consectetur, rerum-->
<!--                            illum.</p>-->
                    </figcaption>
                </figure>
                <div class="aa-product-hvr-content">
                    <a href="#" data-toggle="tooltip"
                       data-placement="top"
                       title="Add to Wishlist"><span
                            class="fa fa-heart-o"></span></a>
                    <!--<a href="#" data-toggle="tooltip" data-placement="top" title="Compare"><span class="fa fa-exchange"></span></a>-->
                    <a href="#" data-toggle2="tooltip"
                       data-placement="top"
                       title="Quick View"
                       data-toggle="modal"
                       data-target=".quick-view-modal-${product.hashed_id}"><span
                            class="fa fa-search"></span></a>
                </div>
                <!-- product badge -->
                <!--<span class="aa-badge aa-sale" href="#">SALE!</span>-->
            </li>
        ` + `        
            <div class="modal fade quick-view-modal-${product.hashed_id}" id="quick-view-modal"
                 tabindex="-1" role="dialog"
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
                                <!-- Modal view slider -->
                                <div class="col-md-6 col-sm-6 col-xs-12">
                                    <div class="aa-product-view-slider">
                                        <div class="simpleLens-gallery-container"
                                             id="demo-${product.hashed_id}">
                                            <div class="simpleLens-container">
                                                <div class="simpleLens-big-image-container">
                                                    <a class="simpleLens-lens-image"
                                                       data-lens-image="${image_url}">
                                                        <!--<img src="img/view-slider/medium/polo-shirt-1.png" class="simpleLens-big-image" width="250" height="300">-->
                                                        <img src="${image_url}"
                                                             class="simpleLens-big-image"
                                                         >
<!--                                                             width="250"-->
<!--                                                             height="300"-->
                                                    </a>
                                                </div>
                                            </div>
                                            <div class="simpleLens-thumbnails-container">
                                                <a href="#"
                                                   class="simpleLens-thumbnail-wrapper"
                                                   data-lens-image="${image_url}"
                                                   data-big-image="${image_url}">
                                                    <img src="${image_url}"
                                                         width="45px"
                                                         height="55px">
                                                </a>
                                               <!--<a href="#"
                                                   class="simpleLens-thumbnail-wrapper"
                                                   data-lens-image="${image_url}"
                                                   data-big-image="${image_url}">
                                                    <img
                                                            src="${image_url}"
                                                            width="45px"
                                                            height="55px">
                                                </a>
    
                                                <a href="#"
                                                   class="simpleLens-thumbnail-wrapper"
                                                   data-lens-image="${image_url}"
                                                   data-big-image="${image_url}">
                                                    <img
                                                            src="${image_url}"
                                                            width="45px"
                                                            height="55px">
                                                </a>-->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <!-- Modal view content -->
                                <style>
                                    .aa-price-block {
                                        display: flex;
                                        justify-content: space-between;                                      
                                        background: #ffef7d;
                                        padding: 20px 10px;                                  
                                    }
                                    .aa-price-block table tr th {
                                        padding: 0 5px 0 0;
                                    }
                                    .aa-price-block table tr td {
                                        padding: 0 0 0 5px;
                                    }
                                    .aa-product-avilability {
                                        background-color: #ff6666;
                                        color: white;
                                        border-radius: 0 0 0 30px;
                                        padding: 10px;
                                    }
                                    .aa-product-avilability span{
                                        color: white !important;
                                    }
                                    .aa-prod-quantity form input {
                                        text-align: center;
                                    }
                                    .aa-prod-quantity {
                                        display: flex;
                                        flex-direction: column;
                                    }
                                    .aa-prod-category {
                                        margin: 0!important;
                                        padding: 10px;                                     
                                        background: #ebff7d;
                                        font-weight: bolder;
                                    }
                                    .aa-prod-quantity form {
                                        margin-top: 10px;
                                        padding: 10px;                                     
                                        background: greenyellow;
                                    }
                                    .unauthorized_order {
                                        font-size: 14px;        
                                        display: none;                                
                                    }
                                    .unauthorized_order a{
                                        font-weight: 700;
                                        color: blue;                                        
                                    }
                                    .aa-product-view-content .part_no{
                                        background: mediumspringgreen;  
                                        padding: 10px;                                       
                                    }
                                </style>
                                <div class="col-md-6 col-sm-6 col-xs-12">
                                    <div class="aa-product-view-content">
                                        <h3>${product.description}</h3>
                                        <h4 class="part_no">Part Number: <strong>${product.part_no}</strong></h4>
                                        
                                        <div class="aa-price-block">
                                            <div>
                                                <table>
                                                <tr>
                                                    <th>Jobber price</th>
                                                    <td>$ ${product.jobbar_price}</td>
                                                </tr>
                                                    <th>Map price</th>
                                                    <td>$ ${product.map_price}</td>
                                                </tr>
                                                    <th>MSRP price</th>
                                                    <td>$ ${product.retail_price}</td>
                                                </tr>
                                                    <th>Your price</th>
                                                    <td>$ ${product.your_price}</td>
                                                </tr>
                                                </table>
                                            </div>
                                            <div>
                                                <p class="aa-product-avilability">
                                                    Avilability:
                                                    <span><span id="live_stock_${product.hashed_id}"></span>In stock</span>
                                                </p>
                                            </div>
                                        </div>
                                        <div class="aa-prod-quantity">
                                            <p class="aa-prod-category">
                                                Brand: 
                                                <a href="/product-list/?brand=${product.manufacturer_hashed_id}" target="_blank">${product.manufacturer_human_readable}</a>
                                                Category: 
                                                <a href="/product-list/?category=${product.category_hashed_id}" target="_blank">${product.category_human_readable}</a>
                                            </p>
                                            <form action=""> 
                                                <label>Quantity: </label>
                                                <input 
                                                    type="number" 
                                                    value="1" 
                                                    min="0" 
                                                    max="0"
                                                    id="product_amount_${product.hashed_id}"
                                                    data-product_hashed_id="${product.hashed_id}"
                                                >
                                            </form>
                                        </div>
                                <!-- <div class="aa-price-block">
                                                <span class="aa-product-view-pric h5">Jobber price: </span>$${product.jobbar_price}<br>
                                                <span class="aa-product-view-pric h5">Map price: </span>$${product.map_price}<br>
                                                <span class="aa-product-view-pric h5">MSRP price: </span>$${product.retail_price}<br>
                                                <span class="aa-product-view-pric h5">Your Cost: </span>$${product.your_price}<br>
                                            <p class="aa-product-avilability">
                                                Avilability:
                                                <span><span id="live_stock_${product.hashed_id}"></span>In stock</span>
                                            </p>
                                        </div>-->
<!--                                        <p>Lorem ipsum dolor-->
<!--                                            sit amet,-->
<!--                                            consectetur-->
<!--                                            adipisicing elit.-->
<!--                                            Officiis animi,-->
<!--                                            veritatis-->
<!--                                            quae repudiandae-->
<!--                                            quod nulla porro-->
<!--                                            quidem, itaque quis-->
<!--                                            quaerat!</p>-->
<!--                                        <h4>Size</h4>-->
<!--                                        <div class="aa-prod-view-size">-->
<!--                                            <a href="#">S</a>-->
<!--                                            <a href="#">M</a>-->
<!--                                            <a href="#">L</a>-->
<!--                                            <a href="#">XL</a>-->
<!--                                        </div>-->
                                        <!--<div class="aa-prod-quantity">
                                            <form action="">
                                                <input 
                                                    type="number" 
                                                    value="0" 
                                                    min="0" 
                                                    max="0"
                                                    id="product_amount_${product.hashed_id}"
                                                    data-product_hashed_id="${product.hashed_id}"
                                                >-->
<!--                                                <select name=""-->
<!--                                                        id="">-->
<!--                                                    <option value="0"-->
<!--                                                            selected="1">-->
<!--                                                        1-->
<!--                                                    </option>-->
<!--                                                    <option value="1">-->
<!--                                                        2-->
<!--                                                    </option>-->
<!--                                                    <option value="2">-->
<!--                                                        3-->
<!--                                                    </option>-->
<!--                                                    <option value="3">-->
<!--                                                        4-->
<!--                                                    </option>-->
<!--                                                    <option value="4">-->
<!--                                                        5-->
<!--                                                    </option>-->
<!--                                                    <option value="5">-->
<!--                                                        6-->
<!--                                                    </option>-->
<!--                                                </select>-->
                                            <!--</form>
                                            <p class="aa-prod-category">
                                                Category: 
                                                <a href="/product-list/?category=${product.category_hashed_id}">${product.category_human_readable}</a>
                                            </p>-->
                                        </div>
                                        <div class="aa-prod-view-bottom" id="special_order_div_${product.hashed_id}" style="display: none">
                                            <img src="/static/base/company/img/special_order.png" style="width: 100%">
                                        </div>
                                        <div class="aa-prod-view-bottom unauthorized_order" id="unauthorized_order_div_${product.hashed_id}">
                                            <p class="text-danger">* You are not authorized to purchase this product due to vendor restrictions.</p>
                                            <p><a href="${product.authorization_form_url}">Click here!</a> to apply for authorization.</p>
                                        </div>
                                        <div class="aa-prod-view-bottom">
                                            <a href="#"
                                               data-id="${product.hashed_id}" data-quantity="1"
                                               class="aa-add-to-cart-btn  add-to-cart-btn-modal cart_btn_${product.hashed_id}"><span
                                                    class="fa fa-cart-plus"></span>Add
                                                To
                                                Cart</a>
                                            <a href="/product-details/${product.hashed_id}/"
                                               class="aa-add-to-cart-btn">View
                                                Details</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div><!-- /.modal-content -->
                </div><!-- /.modal-dialog -->
            </div>
        `
    };

    product = (start=null, price_range='', text_based_search='', other='') => {
        let self = this;
        let sort_by = `sort_by=${$('select[name=sort_by]').val()}`;
        let length = `&length=${$('select[name=length]').val()}`;
        let query_param = sort_by + length;

        if (self.sidebar_selected_category_id !== null) {
            query_param += `&sidebar_category=${self.sidebar_selected_category_id}`;
        }

        if (self.sidebar_selected_brand_id !== null) {
            query_param += `&sidebar_brand=${self.sidebar_selected_brand_id}`;
        }

        if (price_range !== '') {
            query_param += `&price_range=${price_range}`;
        }

        if (text_based_search !== '') {
            query_param += `&text_based_search=${text_based_search}`;
        }

        if (other !== '') {
            query_param += `&${other}`;
        }

        if (start !== null) {
            query_param += `&start=${start}`;
        }

        // make product list empty
        $(`#product_list`).empty();

        $.ajax({
            url: `${product_api_url}?${query_param}`,
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    $(`.aa-product-catg-body ul`).append(
                        self.product_template(value)
                    );
                    if (value.added_from_finale) {
                        self.product_live_stock(value.hashed_id, value.product_id, value.is_authorized, value.authorization_form_url);
                    } else {
                        let stock = value.stock ? value.stock : '0';
                        self.set_availability(false, value.hashed_id, stock, value.is_authorized, value.authorization_form_url)
                    }
                    setTimeout(function (e) {
                        $(`#demo-${value.hashed_id} .simpleLens-thumbnails-container img`).simpleGallery({
                            loading_image: '/static/base/img/slider/ajax-loader.gif'
                        });

                        $(`#demo-${value.hashed_id} .simpleLens-big-image`).simpleLens({
                            loading_image: '/static/base/img/slider/ajax-loader.gif'
                        });
                    }, 2000);
                });
                if (resp.recordsTotal === 0) {
                    $('#product_list').append('<li>No product found</li>')
                } else {
                    let total_pages = Math.ceil(resp.recordsTotal / $('select[name=length]').val());
                    $('#pagination').unbind('page');
                    $('#pagination').twbsPagination({
                        totalPages: total_pages,
                        visiblePages: 5,
                        first: '<span> <i class="ace-icon fa fa-angle-double-left bigger-140"></i> </span>',
                        prev: '<span> <i class="ace-icon fa fa-angle-left bigger-150"></i></i></span>',
                        next: '<span> <i class="ace-icon fa fa-angle-right bigger-150"></i></i></span>',
                        last: '<span> <i class="ace-icon fa fa-angle-double-right bigger-140"></i></span>',
                        onPageClick: function (event, page) {
                        }
                    }).on('page', function (event, page) {
                        start = (page - 1) * resp.data.length;
                        self.product(start, '', self.text_based_search)
                    });
                }
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    on_change_reset_product_list = () => {
        let self = this;
        $('select[name=sort_by], select[name=length]').on('change', function (e) {
            $('#pagination').twbsPagination('destroy');
            self.product(null, '', self.text_based_search)
        });

        setTimeout(function (e) {
            $('#sidebar_category li a').on('click', function (e) {
                self.sidebar_selected_category_id = $(this).data('id');
                self.sidebar_selected_brand_id = null;
                self.sidebar_brand(self.sidebar_selected_category_id);
                $('#sidebar_category li a').removeClass('sidebar_active_product');
                $('.tag-cloud a').removeClass('sidebar_active_brand');
                $(this).addClass('sidebar_active_product');
                $('#pagination').twbsPagination('destroy');
                self.product(null)

            });
        }, 1000);

        setTimeout(function (e) {
            $(document).on('click', '.tag-cloud a', function (e) {
                // self.sidebar_selected_category_id = null;
                self.sidebar_selected_brand_id = $(this).data('id');
                // $('#sidebar_category li a').removeClass('sidebar_active_product');
                $('.tag-cloud a').removeClass('sidebar_active_brand');
                $(this).addClass('sidebar_active_brand');
                $('#pagination').twbsPagination('destroy');
                self.product(null)

            });
        }, 1000);

        // price filter
        var skipSlider = document.getElementById('skipstep');
        noUiSlider.create(skipSlider, {
            range: {
                'min': 0,
                '5%': 100,
                '10%': 200,
                '15%': 300,
                '20%': 400,
                '25%': 500,
                '30%': 600,
                '35%': 700,
                '40%': 800,
                '45%': 900,
                '50%': 1000,
                '55%': 1500,
                '60%': 2000,
                '65%': 2500,
                '70%': 3000,
                '75%': 3500,
                '80%': 4000,
                '85%': 4500,
                '90%': 5000,
                '95%': 10000,
                'max': 15000
            },
            snap: true,
            connect: true,
            start: [0, 15000]
        });
        // for value print
        let lower_price = 0, upper_price = 5000;
        var skipValues = [
          document.getElementById('skip-value-lower'),
          document.getElementById('skip-value-upper')
        ];

        skipSlider.noUiSlider.on('update', function( values, handle ) {
          skipValues[handle].innerHTML = values[handle];
          lower_price = values[0];
          upper_price = values[1];
        });

        $('.aa-filter-btn').on('click', function (e) {
            $('#pagination').twbsPagination('destroy');
            let price_range = `${lower_price},${upper_price}`;
            self.product(null, price_range);
        });
    };

    product_live_stock = (product_hashed_id, product_id, is_authorized, authorization_form_url) => {
        let self = this;
        $.ajax({
            url: product_live_stock_api_url + `?product_id=${product_id}`,
            type: "GET",
            success: function (resp) {
                self.set_availability(true, product_hashed_id, resp.data.available_stock, is_authorized, authorization_form_url)
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    set_availability = (added_from_finale, product_hashed_id, available_stock, is_authorized, authorization_form_url) => {
        // product list notification is BRAND is selected an deale is UNAUTHERIZED
        let unauthorized_brand_message = $('.unauthorized_brand_message');
        if (self.sidebar_selected_brand_id !== null && is_authorized === false) {
            if(!unauthorized_brand_message.is(':visible')) {
                unauthorized_brand_message.show()
            }
            unauthorized_brand_message.find('a').attr('href', authorization_form_url);

        } else {
            if(unauthorized_brand_message.is(':visible')) {
                unauthorized_brand_message.hide()
            }
            unauthorized_brand_message.find('a').attr('href', '#');
        }

        if(is_authorized === false) {
            $(`.cart_btn_${product_hashed_id}`).hide();
            $(`#unauthorized_order_div_${product_hashed_id}`).show();
            $(`#live_stock_${product_hashed_id}`).html(available_stock + " ");
            $(`#product_amount_${product_hashed_id}`).attr("max", available_stock).attr('disabled', 'disabled');
            return;
        }

        if (added_from_finale === false && available_stock === '0') {
            $(`.cart_btn_${product_hashed_id}`).hide();
            $(`#live_stock_${product_hashed_id}`).parent().parent().hide();
            $(`#special_order_div_${product_hashed_id}`).show();
            $(`#product_amount_${product_hashed_id}`).attr("max", available_stock).attr('disabled', 'disabled');
        } else {
            $(`#live_stock_${product_hashed_id}`).html(available_stock + " ");
            $(`#product_amount_${product_hashed_id}`).attr("max", available_stock);
        }
    };

    update_quantity = () => {
        $(document).on('change', '.aa-prod-quantity form input[type=number]', function () {
            let quantity = $(this).val();
            let product_hashed_id = $(this).data('product_hashed_id');
            let cart_button = $('.cart_btn_'+product_hashed_id)[0];
            $(cart_button).attr('data-quantity', quantity);
        });
    };

    grid_view_or_list_view = () => {
        $(document).on('click', '#grid-catg', function () {
            localStorage.setItem('product_list_view_type', 'grid');
        });
        $(document).on('click', '#list-catg', function () {
            localStorage.setItem('product_list_view_type', 'list');
        });

        var product_list_view_type = localStorage.getItem('product_list_view_type');

        if(product_list_view_type === 'list') {
            $(document).ready(function(){
                $(document).find('#list-catg').trigger('click');
            });
        }
    };

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.grid_view_or_list_view();
        this.sidebar_category();
        this.sidebar_brand();
        this.clear_sidebar_selection();
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('category') || urlParams.get('brand') || urlParams.get('q') || urlParams.get('type')) {
            this.on_load_filter_product();
        } else {
            this.product();
        }
        this.banner();
        this.on_change_reset_product_list();
        this.update_quantity();
    }
}


new ProductList().main();
