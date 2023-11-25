/*
* =============================================================================
*                                   PROMOTIONS
* =============================================================================
**/

class BrandPage {

    images = () => {
        let self = this;
        var urlParams = new URLSearchParams(window.location.search);
        if (!urlParams.has('brand')) {
            window.location.href = "/";
        }
        let brand = urlParams.get('brand');

        $.ajax({
            url: brand_page_image_api_url + 'page_wise_images/?brand=' + brand,
            type: "GET",
            success: function (resp) {
                if (resp.data.length === 0) {
                    window.location.href = "/";
                }

                $('.title').text(resp.data.name);
                $('.email').text(resp.data.email);
                $('.tagline').text(resp.data.tagline);
                (resp.data.url !== null) ? $('.url').attr('href', resp.data.url) : $('.url').hide();
                $.map(resp.data.data, function (value, index) {
                    $('.aa-latest-blog-area').append(
                        `
                            <div class="row" id="aa-latest-flyer-area">
                                
                                <a href="${value.redirect_url}" ${value.redirect_url !== '#' ? 'target="_blank"' : 'target="_self"'}>
                                    <img src="/media/${value.image}" alt="${value.title}" width="100%">
                                </a>
                            </div>
                        `
                    )
                });
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
        this.images();
    }
}


new BrandPage().main();
