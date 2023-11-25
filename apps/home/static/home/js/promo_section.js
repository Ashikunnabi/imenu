/*
* =============================================================================
*                                   CAROUSEL
* =============================================================================
**/

class PromoSection {

    /*
    * =========================================================================
    *                       Promo Section in home page
    * =========================================================================
    **/
    promo_left_template = (title, promo, image_url, redirect_url) => {
        return `      
            <a href="${redirect_url}">
                <div class="aa-promo-banner">
                    <img src="${image_url}" alt="img">
                    <!--<img src="img/promo-banner-1.jpg" alt="img">-->
                    <div class="aa-prom-content">
                        <span>${promo}</span>
                        <h4>${title}</h4>
                    </div>
                </div>
            </a>
        `
    };
    promo_right_template = (title, promo, image_url, redirect_url) => {
        return `      
            <div class="aa-single-promo-right">
                <a href="${redirect_url}">
                    <div class="aa-promo-banner">
                        <img src="${image_url}" alt="img">
                        <!--<img src="img/promo-banner-1.jpg" alt="img">-->
                        <div class="aa-prom-content">
                            <span>${promo}</span>
                            <h4>${title}</h4>
                        </div>
                    </div>
                </a>
            </div>
        `
    };

    promo_section = () => {
        let self = this;
        $.ajax({
            url: promo_section_api_url,
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    if (index === 0) {
                        $('.aa-promo-left').append(
                            self.promo_left_template(
                                value.title,
                                value.promo,
                                '/media/'+value.image,
                                value.redirect_url
                            )
                        );
                    } else {
                        $('.aa-promo-right').append(
                            self.promo_right_template(
                                value.title,
                                value.promo,
                                '/media/'+value.image,
                                value.redirect_url
                            )
                        );
                    }
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
        this.promo_section();
    }
}


new PromoSection().main();
