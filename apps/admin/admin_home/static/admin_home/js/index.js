/*
* =============================================================================
*                                   INDEX
* =============================================================================
**/

class Index {
    /*
    * =========================================================================
    *                       Index value setup
    * =========================================================================
    **/

    value_set = () => {
        // edit index form value setup
        $.ajax({
            url: admin_index_api_url,
            type: "get",
            success: function (response) {
                let data = response.data;
                $('#card_1_title').html("ACTIVE PRODUCTS");
                $('#card_1_value').html(data.product.count);

                $('#card_2_title').html("ACTIVE DEALERS");
                $('#card_2_value').html(data.dealer.active_dealer_count);

                $('#card_3_title').html("ACTIVE BRANDS");
                $('#card_3_value').html(data.brand.count);

                $('#card_4_title').html("INACTIVE DEALERS");
                $('#card_4_value').html(data.dealer.inactive_dealer_count);

                $('#card_5_title').html("PENDING ORDERS");
                $('#card_5_value').html(data.order.pending_order_count);

                $('#card_6_title').html("IN PROCESSING ORDERS");
                $('#card_6_value').html(data.order.in_processing_order_count);
            },
            error: function (response) {
                let errors = '';
                $.map(response.responseJSON.details, function (v, i) {
                    $.each(v, function (j, k) {
                        errors += `<li>${i}: ${k}</l1>`;
                    })
                });
                let final_error = `<ul>${errors}</ul>`;
                notify(final_error);
            }
        });
    };

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.value_set();
    }
}


new Index().main();
