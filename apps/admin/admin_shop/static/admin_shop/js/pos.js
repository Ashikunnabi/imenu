/*
* =============================================================================
*                                   POS
* =============================================================================
**/

class POS {
    products = {}
    cart = {}
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    // select_sidebar_option = () => {
    //     $('#sidebar_option_others_a').click();
    //     $('#sidebar_option_others_product_image').addClass('active');
    // };

    /*
    * =========================================================================
    *                       SET PRODUCTS
    * =========================================================================
    **/
    image_url_generator(product) {
        let url = '/static/base/img/no_image.png';
        url = product.image_url ? product.image_url :
            product.image ? '/media/' + product.image : url
        return url;
    }

    set_products = (products) => {
        let self = this
        $("#product_image").html("")
        $.map(products, function (product, i) {
            $("#product_image").append(`
                <div class="product" data-uuid=${product.uuid}
                    title="${product.name}">
                    <!-- <span class="stock">${product.stock}</span> -->
                    <img src="${product.documents.length ? product.documents[0].document.file : ""}">
                    <h4 class="price">${product.prices.length ? product.prices[0].price : "00.00"}</h4>
                    <p>${product.name}</p>
                </div>
            `)
        })
    }

    /*
    * =========================================================================
    *                       FETCH PRODUCTS
    * =========================================================================
    **/
    fetch_products = () => {
        let self = this
        $.ajax({
            url: list_api_url,
            type: "GET",
            success: function (resp) {
                self.products = resp
                self.set_products(resp.data)
            },
            error: function (response) {
                notify(response.responseText, 'error', 5000);
            }
        });
    }

    /*
    * =========================================================================
    *                       REFRESH PRODUCTS
    * =========================================================================
    **/
    refresh_products = () => {
        let self = this
        self.fetch_products()
        // $(document).on("change", "#warehouse", function (e) {
        //     self.call_products()
        // })
        // $(document).on("change", "#sales_order", function (e) {
        //     self.call_products()
        // })

        // $(document).on("click", "#refresh_products", function (e) {
        //     self.call_products()
        // })
    }

    /*
    * =========================================================================
    *                       FETCH PRODUCTS
    * =========================================================================
    **/
    fetch_order = () => {
        let self = this
        $.ajax({
            url: shop_order_pos_api_url,
            type: "GET",
            success: function (resp) {
                self.order = resp
            },
            error: function (response) {
                notify(response.responseText, 'error', 5000);
            }
        });
    }
    /*
    * =========================================================================
    *                       SET CART
    * =========================================================================
    **/
    set_cart = (products) => {
        let self = this
        $("#cart").html("")
        $.map(products, function (product, i) {
            $("#cart").append(`
                <tr>
                    <td class="product-name">${product.product_id}</td>
                    <td class="product-quantity">
                        <input type="number" value="${product.quantity}" class="cart_product_quantity" id="cart_product_quantity_${product.product_uuid}">
                    </td>
                    <td>${product.unit_price}</td>
                    <td>${product.price}</td>
                    <td><i class="fas fa-trash cart_product_delete" style="color: red;cursor:pointer" id="cart_product_delete_${product.product_uuid}"></i></td>
                </tr>
            `)
        })
    }
    /*
    * =========================================================================
    *                       SET CART SUMMARY
    * =========================================================================
    **/
    set_cart_summary = (order) => {
        let self = this
        $(".cart_subtotal").text(order.sub_total)
        $(".cart_total").text(order.total)
        $(".cart_discount").val(order.discount)
        $(".cart_tax").val(order.tax)
    }

    /*
    * =========================================================================
    *                       ADD TO CART BY PRODUCT IMAGE CLICK
    * =========================================================================
    **/
    fetch_cart = () => {
        let self = this
        $.ajax({
            url: shop_order_pos_api_url,
            type: "GET",
            success: function (resp) {
                self.cart = resp
                let data = resp.data[0]
                self.set_cart(data.order_lines)
                self.set_cart_summary(data)
            },
            error: function (response) {
                notify(response.responseText, 'error', 5000);
            }
        });
    }

    /*
    * =========================================================================
    *                       ADD TO CART BY PRODUCT IMAGE CLICK
    * =========================================================================
    **/
    add_to_cart = () => {
        let self = this

        // on click product add to cart
        $(document).on("click", ".product", function (e) {
            let data = {}
            data.type = "orderline"
            data.product_uuid = $(this).attr("data-uuid")
            data.quantity = parseInt($(`#cart_product_quantity_${$(this).attr("data-uuid")}`).val() || 0) + 1
            $.ajax({
                url: shop_order_pos_api_url,
                type: "POST",
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify("Success", 'success', 5000);
                    self.fetch_cart();
                },
                error: function (response) {
                    notify(response.responseText, 'error', 5000);
                }
            });
        })

        // on change on cart quantity 
        $(document).on("keyup", ".cart_product_quantity", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                let data = {}
                data.type = "orderline"
                data.product_uuid = $(this).attr("id").replace("cart_product_quantity_", "")
                data.quantity = parseInt($(`#cart_product_quantity_${data.product_uuid}`).val())
                $.ajax({
                    url: shop_order_pos_api_url,
                    type: "POST",
                    data: JSON.stringify(data),
                    dataType: 'json',
                    contentType: "application/json",
                    success: function (resp) {
                        notify("Success", 'success', 5000);
                        self.fetch_cart();
                    },
                    error: function (response) {
                        notify(response.responseText, 'error', 5000);
                    }
                });
            }
        })

        // delete cart item 
        $(document).on("click", ".cart_product_delete", function (e) {
            let data = {}
            data.type = "orderline"
            data.product_uuid = $(this).attr("id").replace("cart_product_delete_", "")
            $.ajax({
                url: shop_order_pos_api_url,
                type: "DELETE",
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify("Success", 'success', 5000);
                    self.fetch_cart();
                },
                error: function (response) {
                    notify(response.responseText, 'error', 5000);
                }
            });
        })


        // add discount 
        $(document).on("click", ".cart_discount, .cart_tax", function (e) {
            $(this).select();
        })

        $(document).on("keyup", ".cart_discount", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                let data = {}
                data.type = "discount"
                data.quantity = 1
                data.unit_price = $(`.cart_discount`).val()
                $.ajax({
                    url: shop_order_pos_api_url,
                    type: "POST",
                    data: JSON.stringify(data),
                    dataType: 'json',
                    contentType: "application/json",
                    success: function (resp) {
                        notify("Success", 'success', 5000);
                        self.fetch_cart();
                    },
                    error: function (response) {
                        notify(response.responseText, 'error', 5000);
                    }
                });
            }
        })


        // add tax 
        $(document).on("keyup", ".cart_tax", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                let data = {}
                data.type = "tax"
                data.quantity = 1
                data.unit_price = $(`.cart_tax`).val()
                $.ajax({
                    url: shop_order_pos_api_url,
                    type: "POST",
                    data: JSON.stringify(data),
                    dataType: 'json',
                    contentType: "application/json",
                    success: function (resp) {
                        notify("Success", 'success', 5000);
                        self.fetch_cart();
                    },
                    error: function (response) {
                        notify(response.responseText, 'error', 5000);
                    }
                });
            }
        })
    }

    /*
    * =========================================================================
    *                       COMPLETE ORDER
    * =========================================================================
    **/
    complete_order = () => {
        let self = this
        $(document).on("click", "#complete_order", function (e) {
            $.ajax({
                url: shop_complete_order_api_url,
                type: "POST",
                // data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify("Success", 'success', 3000);
                    let code = `H0000${resp.id}`
                    self.search_order(code)
                    $('#print_order_modal').on('hidden.bs.modal', function () {
                        setTimeout(() => { window.location.reload(); }, 1000);
                    })
                },
                error: function (response) {
                    notify(response.responseText, 'error', 5000);
                }
            });
        })
    }

    /*
    * =========================================================================
    *                       PRINT ORDER
    * =========================================================================
    **/
    search_order = (code) => {
        let self = this
        $.ajax({
            url: shop_order_pos_search_api_url + `?code=${code}`,
            type: "GET",
            // data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            success: function (resp) {
                let data = resp.data[0];
                notify("Success", 'success', 3000);
                $('#print_order_modal').modal('show');
                $("#print_order_modalTitle").text(`H0000${data.id}`)
                $(".print_order_modal_body_shop_info .name").text(`${data.shop.name}`)
                $(".print_order_modal_body_shop_info .address").text(`${data.shop.location}`)
                $(".print_order_modal_body_shop_info .phone_numbers").text(`${data.shop.phone_numbers}`)
                $(".print_order_modal_body_shop_info .order_header .order_no").text(`Order ID: H0000${data.id}`)
                $(".print_order_modal_body_shop_info .order_header .datetime").text(`Date: ${moment(data.created_at).format('lll')}`)
                $("#print_order_products").html("")
                $.map(data.order_lines, function (product, i) {
                    $("#print_order_products").append(`
                            <tr>
                                <td class="product-name">${product.product_id}</td>
                                <td class="product-quantity">${product.quantity}</td>
                                <td>${product.unit_price}</td>
                                <td>${product.price}</td>
                            </tr>
                        `)
                })
                $(".print_order_subtotal").text(data.sub_total)
                $(".print_order_total").text(data.total)
                $(".print_order_discount").val(data.discount)
                $(".print_order_tax").val(data.tax)

                $(document).ready(function () {
                    $(document).on('click', '#print_order_modal_print_btn', function () {
                        printJS({
                            printable: 'print_order_modal_body',
                            type: 'html',
                            maxWidth: 219, // the width of your paper
                            style: `
                                body {max-width: 58mm;}
                                table tr th, table tr td{vertical-align:top;border-top:1px solid #e3e6f0}
                                table tr th, table tr td{padding:0.5rem 0.75rem;}
                                table tfoot tr td{padding:0 0.75rem;}
                                #print_order_modal_table {text-align: left;font-size:10pt}
                                .print_order_modal_body_shop_info h4{margin-bottom: 0;}
                                .print_order_modal_body_shop_info {text-align: center; width: 70mm;}
                                `
                        })
                    });
                });
            },
            error: function (response) {
                notify(response.responseText, 'error', 5000);
            }
        });
    }

    /*
    * =========================================================================
    *                       DELETE ORDER
    * =========================================================================
    **/
    delete_order = () => {
        let self = this
        $(document).on("click", "#delete_order", function (e) {
            $.ajax({
                url: shop_delete_order_api_url,
                type: "POST",
                // data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify("Success", 'success', 3000);
                    setTimeout(() => { window.location.reload(); }, 3000);
                },
                error: function (response) {
                    notify(response.responseText, 'error', 5000);
                }
            });
        })
    }

    barcode_scan = () => {
        let self = this
        $(document).on("keyup", "#barcode_scan_data", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                $.ajax({
                    url: list_api_url + `?q=${$("#barcode_scan_data").val()}`,
                    type: "GET",
                    success: function (resp) {
                        self.products = resp
                        self.set_products(resp.data)

                        if (!resp.data.length) {
                            notify("Failed: Not found", 'error', 5000);
                        } else {
                            $("#barcode_scan_data").val("")
                            if ($("#auto_add_to_cart").is(":checked")) {
                                $(".product").trigger("click")
                                self.refresh_products()
                            }
                        }
                    },
                    error: function (response) {
                        notify(response.responseText, 'error', 5000);
                    }
                });
            }
        })
    }

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        // this.select_sidebar_option();
        let self = this
        self.refresh_products();
        self.add_to_cart();
        self.fetch_order();
        self.fetch_cart();
        self.barcode_scan();
        self.complete_order();
        self.delete_order();
    }
}


new POS().main();
