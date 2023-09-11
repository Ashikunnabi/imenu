/*
* =============================================================================
*                                   CATEGORY
* =============================================================================
**/

class Category {

    categories = () => {
        let self = this;
        $.ajax({
            url: category_api_url,
            type: "GET",
            success: function (resp) {
                // set categories at home page
                let html = '';
                $.map(resp.data, function (value, index) {
                    let url = value.image !== null && value.image !== "" ? '/media/' + value.image : '/static/base/img/no_image.png';
                    html += `
                    <a href="/product-list/?category=${value.hashed_id}" style="width:200px;height:200px;text-align:center;">
                        <img src=${url} style="width:75px;">
                        <p>${value.name}</p>
                    </a>
                    `;
                });
                $('.aa-category-area div').append(html);
            },
            error: function (response) {
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
        this.categories();
    }
}


new Category().main();
