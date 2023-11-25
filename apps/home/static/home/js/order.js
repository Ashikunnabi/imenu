/*
* =============================================================================
*                                   ORDER
* =============================================================================
**/

class Order {

    added_to_cart = () => {
        let self = this;
        $(document).on('click', '.aa-add-card-btn, .add-to-cart-btn-modal', function (e) {
            e.preventDefault();
            $(this).text('Processing');
            let product_hashed_id = $(this).data('id');
            let product_quantity = $(this).data('quantity');
            self.add_to_cart($(this), product_hashed_id, product_quantity);
        });
    };

    add_to_cart = (product_object, product_hashed_id, product_quantity) => {
        let self = this;
        let data = {
            product: product_hashed_id,
            quantity: product_quantity
        };
        $.ajax({
            url: cart_api_url,
            type: "POST",
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            success: function (resp) {
                product_object.text('Successfully added');
            },
            error: function (response) {
                let data = response.responseJSON.detail;
                product_object.text(data);
                console.log(response)
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
        this.added_to_cart();
    }
}


new Order().main();
