/*
* =============================================================================
*                                   PRODUCT
* =============================================================================
**/

class PopularCategory {

    /*
    * =========================================================================
    *                       PopularCategory in home page
    * =========================================================================
    **/

    image_url_generator(product) {
        let url = '/static/base/img/no_image.png';
        url = product.image_url ? product.image_url :
            product.image ? '/media/' + product.image : url
        return url;
    }

    latest_product_category_template = (product) => {
        let image_url = product.image_url ? product.image_url :
            product.image ? '/media/' + product.image : '/static/base/img/no_image.png';
        return `            
            <li>
                <figure>
                    <a class="aa-product-img" href="product-details/${product.hashed_id}/">
                        <img
                            src="${image_url}"
                            alt="polo shirt img"
                            width="251"
                            height="300"
                        >
                    </a>
                    <a class="aa-add-card-btn latest_product_cart_btn_${product.hashed_id}" href="#" data-id="${product.hashed_id}" data-quantity="1">
                        <span class="fa fa-shopping-cart"></span>
                        Add To Cart
                    </a>
                    <figcaption>
                        <h4 class="aa-product-title">
                            <a href="product-details/${product.hashed_id}/">${product.description}</a>
                        </h4>
                        <!-- <span class="aa-product-price">$${product.jobbar_price}
                         ${product.jobbar_price ? '<span class="aa-product-price"><del>$${product.jobbar_price}</del></span>' : ''} -->
                    </figcaption>
                </figure>
                <div class="aa-product-hvr-content">
                    <a 
                        href="#" 
                        data-toggle="tooltip"
                        data-placement="top"
                        title="Add to Wishlist"
                    >
                        <span class="fa fa-heart-o"></span>
                    </a>
                    <!-- <a href="#" data-toggle="tooltip" data-placement="top" title="Compare"><span class="fa fa-exchange"></span></a>-->
                    <a 
                        href="#" 
                        data-toggle2="tooltip"                       
                        data-placement="top"                       
                        title="Quick View"                       
                        data-toggle="modal"                      
                        data-target=".latest_product_quick-view-modal-${product.hashed_id}"
                    >
                        <span class="fa fa-search"></span>
                    </a>
                </div>
                <!-- product badge -->
                <!--<span class="aa-badge aa-sale" href="#">SALE!</span>-->
                <!--<span class="aa-badge aa-hot" href="#">HOT!</span>-->
            </li>
        `
    };

    latest_product_category_modal_template = (product) => {
        let self = this;
        let image_url = self.image_url_generator(product)
        return  `<div 
            class="modal fade latest_product_quick-view-modal-${product.hashed_id}" 
            id="quick-view-modal"
            tabindex="-1" role="dialog"
            aria-labelledby="myModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-body">
                        <button 
                            type="button" 
                            class="close"
                            data-dismiss="modal"
                            aria-hidden="true"
                        >
                            &times;                            
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
                                            <span id="latest_product_live_stock_${product.hashed_id}"></span>
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
                                                id="latest_product_product_amount_${product.hashed_id}"
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
                                <div class="aa-prod-view-bottom" id="latest_product_special_order_div_${product.hashed_id}" style="display: none">
                                    <img src="/static/base/company/img/special_order.png" style="width: 100%">
                                </div>

                                <!-- UNAUTHORIZED DECLARATION  -->
                                <div class="aa-prod-view-bottom unauthorized_order" id="unauthorized_order_div_${product.hashed_id}">
                                    <p class="text-danger">* You are not authorized to purchase this product due to vendor restrictions.</p>
                                    <p><a href="${product.authorization_form_url}">Click here!</a> to apply for authorization.</p>
                                </div>

                                <!-- ADD TO CART FOR ORDER WITH WISHLIST -->
                                <div class="aa-prod-view-bottom">
                                    <a class="aa-add-to-cart-btn aa-add-card-btn latest_product_cart_btn_${product.hashed_id}"
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
    
    depricated_latest_product_category_modal_template = (product) => {
        let image_url = product.image_url ? product.image_url :
            product.image ? '/media/' + product.image : '/static/base/img/no_image.png';
        return `        
            <div class="modal fade latest_product_quick-view-modal-${product.hashed_id}" id="quick-view-modal"
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
                                             id="latest_product_demo-${product.hashed_id}">
                                            <div class="simpleLens-container">
                                                <div class="simpleLens-big-image-container">
                                                    <a class="simpleLens-lens-image"
                                                       data-lens-image="${image_url}">
                                                        <img src="${image_url}"
                                                             class="simpleLens-big-image">
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
<!--                                                <a href="#"-->
<!--                                                   class="simpleLens-thumbnail-wrapper"-->
<!--                                                   data-lens-image="${image_url}"-->
<!--                                                   data-big-image="${image_url}">-->
<!--                                                    <img src="${image_url}">-->
<!--                                                </a>-->

<!--                                                <a href="#"-->
<!--                                                   class="simpleLens-thumbnail-wrapper"-->
<!--                                                   data-lens-image="${image_url}"-->
<!--                                                   data-big-image="${image_url}">-->
<!--                                                    <img src="${image_url}">-->
<!--                                                </a>-->
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
                                <div class="col-md-6 col-sm-6 col-xs-12" style="text-align: left">
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
                                                    <span><span id="latest_product_live_stock_${product.hashed_id}"></span>In stock</span>
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
                                                    id="latest_product_product_amount_${product.hashed_id}"
                                                    data-product_hashed_id="${product.hashed_id}"
                                                >
                                            </form>
                                        </div>
                                        <!-- <div class="aa-price-block" style="text-align: left">
                                                <span class="aa-product-view-pric h5">Jobber price: </span>$${product.jobbar_price}<br>
                                                <span class="aa-product-view-pric h5">Map price: </span>$${product.map_price}<br>
                                                <span class="aa-product-view-pric h5">MSRP price: </span>$${product.retail_price}<br>
                                                <span class="aa-product-view-pric h5">Your Cost: </span>$${product.your_price}<br>
                                            <p class="aa-product-avilability">
                                                Avilability:
                                                <span><span id="latest_product_live_stock_${product.hashed_id}"></span>In stock</span>
                                            </p>
                                        </div>-->
<!--{#                                                        <p>Lorem ipsum dolor-->
<!--{#                                                            sit amet,-->
<!--{#                                                            consectetur-->
<!--{#                                                            adipisicin-->
<!--{#                                                            Officiis animi,-->
<!--{#                                                            veritatis quae-->
<!--{#                                                            repudiandae quod-->
<!--{#                                                            nulla porr-->
<!--{#                                                            itaque quis-->
<!--{#                                                            quaerat!</p>-->
<!--{#                                                        <h4>Size</h4>-->
<!--{#                                                        <div class="aa-prod-view-size">-->
<!--{#                                                            <a href="#">S</a>-->
<!--{#                                                            <a href="#">M</a>-->
<!--{#                                                            <a href="#">L</a>-->
<!--{#                                                            <a href="#">XL</a>-->
<!--{#                                                        </div>-->
                                        <!--<div class="aa-prod-quantity" style="text-align: left">
                                            <form action="">
                                                <input 
                                                    type="number" 
                                                    value="1" 
                                                    min="0" 
                                                    max="0"
                                                    id="latest_product_product_amount_${product.hashed_id}"
                                                    data-product_hashed_id="${product.hashed_id}"
                                                >-->
<!--{                                                               <select name=""-->
<!--{#                                                                      id="">-->
<!--{#                                                                  <option value="0"-->
<!--{#                                                                          selected="1">-->
<!--{#                                                                      1-->
<!--{#                                                                  </option>-->
<!--{#                                                                  <option value="1">-->
<!--{#                                                                      2-->
<!--{#                                                                  </option>-->
<!--{#                                                                  <option value="2-->
<!--{#                                                                      3-->
<!--{#                                                                  </option>-->
<!--{#                                                                  <option value="3">-->
<!--{#                                                                      4-->
<!--{#                                                                  </option>-->
<!--{#                                                                  <option value="4">-->
<!--{#                                                                      5-->
<!--{#                                                                  </option>-->
<!--{#                                                                  <option value="5">-->
<!--{#                                                                      6-->
<!--{#                                                                  </option>-->
<!--{#                                                              </select>-->
                                            <!--</form>
                                            <p class="aa-prod-category">
                                                Category: 
                                                <a href="/product-list/?category=${product.category_hashed_id}">${product.category_human_readable}</a>
                                            </p>-->
                                        </div>
                                        <div class="aa-prod-view-bottom" id="latest_product_special_order_div_${product.hashed_id}" style="display: none">
                                            <img src="/static/base/company/img/special_order.png" style="width: 100%">
                                        </div>
                                        <div class="aa-prod-view-bottom unauthorized_order" id="unauthorized_order_div_${product.hashed_id}">
                                            <p class="text-danger">* You are not authorized to purchase this product due to vendor restrictions.</p>
                                            <p><a href="${product.authorization_form_url}">Click here!</a> to apply for authorization.</p>
                                        </div>
                                        <div class="aa-prod-view-bottom">
                                            <a href="#"
                                               data-id="${product.hashed_id}" data-quantity="1"
                                               class="aa-add-to-cart-btn add-to-cart-btn-modal latest_product_cart_btn_${product.hashed_id}"><span
                                                    class="fa fa-shopping-cart"></span>Add
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

    latest_product = () => {
        let self = this;
        $.ajax({
            url: latest_product_api_url + '?length=4',
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    $('#popular ul').append(
                        self.latest_product_category_template(value)
                    );
                    let latest_product_category_modal = self.latest_product_category_modal_template(value);
                    $('#latest_product_category_modals').append(latest_product_category_modal);
                    if (value.added_from_finale) {
                        self.product_live_stock(value.hashed_id, value.product_id, value.is_authorized);
                    } else {
                        let stock = value.stock ? value.stock : '0';
                        self.set_availability(false, value.hashed_id, stock, value.is_authorized)
                    }

                    setTimeout(function (e) {
                        $(`#latest_product_demo-${value.hashed_id} .simpleLens-thumbnails-container img`).simpleGallery({
                            loading_image: '/static/base/img/slider/ajax-loader.gif'
                        });

                        $(`#latest_product_demo-${value.hashed_id} .simpleLens-big-image`).simpleLens({
                            loading_image: '/static/base/img/slider/ajax-loader.gif'
                        });
                    }, 2000);
                });
                $('.aa-popular-slider').slick("unslick");
                $('.aa-popular-slider').slick({
                    dots: false,
                    infinite: false,
                    speed: 300,
                    slidesToShow: 4,
                    slidesToScroll: 4,
                    responsive: [
                        {
                            breakpoint: 1024,
                            settings: {
                                slidesToShow: 3,
                                slidesToScroll: 3,
                                infinite: true,
                                dots: true
                            }
                        },
                        {
                            breakpoint: 600,
                            settings: {
                                slidesToShow: 2,
                                slidesToScroll: 2
                            }
                        },
                        {
                            breakpoint: 480,
                            settings: {
                                slidesToShow: 1,
                                slidesToScroll: 1
                            }
                        }
                        // You can unslick at a given breakpoint now by adding:
                        // settings: "unslick"
                        // instead of a settings object
                    ]
                });
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    product_live_stock = (product_hashed_id, product_id, is_authorized) => {
        let self = this;
        $.ajax({
            url: product_live_stock_api_url + `?product_id=${product_id}`,
            type: "GET",
            success: function (resp) {
                self.set_availability(true, product_hashed_id, resp.data.available_stock, is_authorized);
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    set_availability = (added_from_finale, product_hashed_id, available_stock, is_authorized) => {

        if(is_authorized === false) {
            $(`.latest_product_cart_btn_${product_hashed_id} `).hide();
            $(`#unauthorized_order_div_${product_hashed_id}`).show();
            $(`#product_amount_${product_hashed_id}`).attr("max", available_stock).attr('disabled', 'disabled');
            return;
        }

        if (added_from_finale === false && available_stock === '0') {
            $(`.latest_product_cart_btn_${product_hashed_id} `).hide();
            $(`#latest_product_live_stock_${product_hashed_id}`).parent().parent().hide();
            $(`#latest_product_special_order_div_${product_hashed_id}`).show();
            $(`#latest_product_product_amount_${product_hashed_id}`).attr("max", available_stock).attr('disabled', 'disabled');
        } else {
            $(`#latest_product_live_stock_${product_hashed_id}`).html(available_stock + " ");
            $(`#latest_product_product_amount_${product_hashed_id}`).attr("max", available_stock);
        }
    };



    latest_brand_template = (data) => {
        let image_url = data.image ? '/media/' + data.image : '/static/base/img/no_image.png';
        return `            
            <li>
                <figure>
                    <a class="aa-product-img" href=/product-list/?brand=${data.hashed_id}>
                        <img
                            src="${image_url}"
                            alt=""
                            width="251"
                            height="300"
                        >
                    </a>
<!--                    <a class="aa-add-card-btn" href="#">-->
<!--                        <span class="fa fa-shopping-cart"></span>-->
<!--                        Add To Cart-->
<!--                    </a>-->
                    <figcaption>
                        <h4 class="aa-product-title">
                            <a href=/product-list/?brand=${data.hashed_id}>${data.name}</a>
                        </h4>
                        <!-- <span class="aa-product-price">$${data.jobbar_price}
                         // ${data.jobbar_price ? '<span class="aa-product-price"><del>$${data.jobbar_price}</del></span>' : ''} -->
                    </figcaption>
<!--                </figure>-->
<!--                <div class="aa-product-hvr-content">-->
<!--                    <a -->
<!--                        href="#" -->
<!--                        data-toggle="tooltip"-->
<!--                        data-placement="top"-->
<!--                        title="Add to Wishlist"-->
<!--                    >-->
<!--                        <span class="fa fa-heart-o"></span>-->
<!--                    </a>-->
                    <!-- <a href="#" data-toggle="tooltip" data-placement="top" title="Compare"><span class="fa fa-exchange"></span></a>-->
<!--                    <a -->
<!--                        href="#" -->
<!--                        data-toggle2="tooltip"                       -->
<!--                        data-placement="top"                       -->
<!--                        title="Quick View"                       -->
<!--                        data-toggle="modal"                      -->
<!--                        data-target=".latest_product_quick-view-modal-${data.hashed_id}"-->
<!--                    >-->
<!--                        <span class="fa fa-search"></span>-->
<!--                    </a>-->
                </div>
                <!-- product badge -->
                <!--<span class="aa-badge aa-sale" href="#">SALE!</span>-->
                <!--<span class="aa-badge aa-hot" href="#">HOT!</span>-->
            </li>
        `
    };

    latest_brand = () => {
        let self = this;
        $.ajax({
            url: brand_images_api_url + '?length=4&show_latest=1',
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    $('#featured ul').append(
                        self.latest_brand_template(value)
                    );
                });
                $('.aa-featured-slider').slick("unslick");
                $('.aa-featured-slider').slick({
                    dots: false,
                    infinite: false,
                    speed: 300,
                    slidesToShow: 4,
                    slidesToScroll: 4,
                    responsive: [
                        {
                            breakpoint: 1024,
                            settings: {
                                slidesToShow: 3,
                                slidesToScroll: 3,
                                infinite: true,
                                dots: true
                            }
                        },
                        {
                            breakpoint: 600,
                            settings: {
                                slidesToShow: 2,
                                slidesToScroll: 2
                            }
                        },
                        {
                            breakpoint: 480,
                            settings: {
                                slidesToShow: 1,
                                slidesToScroll: 1
                            }
                        }
                        // You can unslick at a given breakpoint now by adding:
                        // settings: "unslick"
                        // instead of a settings object
                    ]
                });
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    update_quantity = () => {
        $(document).on('change', '.aa-prod-quantity form input[type=number]', function () {
            let quantity = $(this).val();
            let product_hashed_id = $(this).data('product_hashed_id');
            let cart_button = $('.latest_product_cart_btn_'+product_hashed_id)[0];
            $(cart_button).attr('data-quantity', quantity);
        });
    };

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.latest_product();
        this.latest_brand();
        this.update_quantity();
    }
}


new PopularCategory().main();
