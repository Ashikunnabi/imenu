/*
* =============================================================================
*                                   POS
* =============================================================================
**/

class POS {
    response = {}
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
    *                       WAREHOUSE SEARCH
    * =========================================================================
    **/
    warehouse = () => {
        $("#warehouse").select2({
            dropdownParent: $("#pos_section"),
            minimumInputLength: 3,
            ajax: {
                url: warehouse_api_url,
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.uuid,
                            text: `${v.name} - ${v.location}`,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });
    }

    /*
    * =========================================================================
    *                       SO SEARCH
    * =========================================================================
    **/
    sales_order = () => {
        $("#sales_order").select2({
            dropdownParent: $("#pos_section"),
            minimumInputLength: 3,
            ajax: {
                url: sales_order_api_url,
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.uuid,
                            text: `${v.number}`,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });
    }

    /*
    * =========================================================================
    *                       SET PRODUCTS
    * =========================================================================
    **/
    set_products = (products) => {
        let self = this
        $("#products table tbody").html("")
        $("#product_image").html("")
        $.map(products, function (product, i) {
            $("#products table tbody").append(`
                <tr style="background:${(product.pending == 0) ? '#d3ffd3' : '#ffdada'}">
                    <td>${product.product_id}</td>
                    <td>${product.price}</td>
                    ${(product.pending == 0) ? `<td>
                        <span 
                            style="background:gray;color:white;padding:5px 10px;border-radius:4px;margin-right:5px"
                            title="Pending quantity for delivery"
                        >${product.pending}</span>
                    </td>` : `<td>
                        <span 
                            style="background:gray;color:white;padding:5px 10px;border-radius:4px;margin-right:5px"
                            title="Pending quantity for delivery"
                        >${product.pending}</span>
                        <input type="text" max=${product.pending} style="width:60px;text-align:center;" id="cart_${product.uuid}" value="0">
                    </td>
                    `}
                    <td>${product.subtotal}</td>
                </tr>
            `)
            self.set_product_image(product)
        })
    }

    /*
    * =========================================================================
    *                       PRODUCT IMAGE
    * =========================================================================
    **/
    set_product_image = (product) => {
        let self = this
        let class_name = (product.pending == 0) ? "" : "right_products"


        $.ajax({
            url: product_api_url + `${product.uuid}/`,
            type: "GET",
            success: function (resp) {
                $("#product_image").append(`
                    <div style="width:200px;height:180px;cursor:pointer" class="${class_name}" data-uuid="${resp.uuid}" data-product_id="${resp.product_id}">
                        <img src="${resp.image_url}"
                            width="200px" height="150px">
                        <p style="text-align:center;">${resp.product_id}</p>
                    </div>
                `)
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
    add_to_left_cart = () => {
        let self = this
        $(document).on("click", ".right_products", function (e) {
            let uuid = $(this).attr("data-uuid")
            let cart_uuid = `cart_${$(this).attr("data-uuid")}`
            let current_product_value_int = parseInt($(`#${cart_uuid}`).val())
            let current_product_max_int = parseInt($(`#${cart_uuid}`).attr("max"))

            if (current_product_max_int > current_product_value_int) {
                $(`#${cart_uuid}`).val(current_product_value_int + 1)
            } else {
                notify(`More than ${current_product_max_int} not allowed`, 'error', 5000);
            }
        })

    }

    /*
    * =========================================================================
    *                       FETCH PRODUCTS
    * =========================================================================
    **/
    fetch_products = () => {
        let self = this
        let sales_order_uuid = $("#sales_order").val()

        $.ajax({
            url: sales_order_api_url + `${sales_order_uuid}/`,
            type: "GET",
            success: function (resp) {
                self.response = resp
                self.set_products(resp.data.products)
            },
            error: function (response) {
                notify(response.responseText, 'error', 5000);
            }
        });
    }

    /*
    * =========================================================================
    *                       CALL PRODUCTS
    * =========================================================================
    **/
    call_products = () => {
        let self = this
        let warehouse_uuid = $("#warehouse").val()
        let sales_order_uuid = $("#sales_order").val()

        if (warehouse_uuid === "Search warehouse") {
            notify("Select warehouse", 'error', 5000);
            return
        }

        if (sales_order_uuid === "Search sales order") {
            notify("Select sales order", 'error', 5000);
            return
        }

        self.fetch_products()
    }

    /*
    * =========================================================================
    *                       REFRESH PRODUCTS
    * =========================================================================
    **/
    refresh_products = () => {
        let self = this
        $(document).on("change", "#warehouse", function (e) {
            self.call_products()
        })
        $(document).on("change", "#sales_order", function (e) {
            self.call_products()
        })

        $(document).on("click", "#refresh_products", function (e) {
            self.call_products()
        })
    }

    /*
    * =========================================================================
    *                       UPDATE STOCK
    * =========================================================================
    **/
    update_stock = () => {
        let self = this

        $(document).on('click', '#update_stock_submit_button', function (e) {
            e.preventDefault()
            let warehouse_uuid = $("#warehouse").val()
            let sales_order_uuid = $("#sales_order").val()

            if (warehouse_uuid === "Search warehouse") {
                notify("Select warehouse", 'error', 5000);
                return
            }

            if (sales_order_uuid === "Search sales order") {
                notify("Select sales order", 'error', 5000);
                return
            }

            $.each(self.response.data.products, function (i, v) {
                let warehouses = []
                if (v.pending == 0) {
                    return
                }

                if ([0, "0", ""].indexOf($(`#cart_${v.uuid}`).val()) > -1) {
                    return
                }

                if (parseInt($(`#cart_${v.uuid}`).val()) > parseInt($(`#cart_${v.uuid}`).attr("max"))) {
                    notify('Selling quantity can not be more than pending quantity', 'error', 5000);
                    return
                }

                // get warehouses info 
                warehouses.push({
                    id: $("#warehouse").select2('data')[0].other.id,
                    uuid: $("#warehouse").select2('data')[0].other.uuid,
                    stock: parseInt($(`#cart_${v.uuid}`).val())
                })

                let data = {
                    id: v.id,
                    uuid: sales_order_uuid,
                    product_id: v.product_id,
                    unit_price: v.price,
                    current_delivered: parseInt($(`#cart_${v.uuid}`).val()),
                    warehouses: warehouses
                }

                $.ajax({
                    url: stock_transaction_api_url,
                    type: "POST",
                    data: JSON.stringify(data),
                    dataType: 'json',
                    contentType: "application/json",
                    success: function (resp) {
                        notify("Stock updated successfully", 'success', 3000);
                        setTimeout(function (e) {
                            window.location.reload()
                        }, 3000)
                    },
                    error: function (response) {
                        notify(response.responseText, 'error', 5000);
                    }
                });
            })
        })
    }

    barcode_scan = () => {
        $(document).on("keyup", "#barcode_scan_data", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                $.map($(document).find(".right_products"), function (v, i) {
                    if ($(v).attr("data-product_id") == $("#barcode_scan_data").val()) {
                        $(v).trigger("click")                        
                    }
                    $("#barcode_scan_data").val("")
                })
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
        self.warehouse();
        self.sales_order();
        self.refresh_products();
        self.add_to_left_cart();
        self.update_stock();
        self.barcode_scan();
    }
}


new POS().main();
