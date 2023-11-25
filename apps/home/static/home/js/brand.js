/*
* =============================================================================
*                                   BRAND
* =============================================================================
**/

class Brand {

    brand = () => {
        let self = this;
        $.ajax({
            url: brand_images_api_url,
            type: "GET",
            success: function (resp) {
                let brands = [];
                $.map(resp.data, function (value, index) {
                    if (value.image !== null) {
                        brands.push(
                            `                            
                            <li>
                                <a href=/product-list/?brand=${value.hashed_id}>
                                    <img
                                        src="/media/${value.image}"
                                        alt=""
                                    >
                                </a>
                            </li>
                            `
                        );
                    }
                });
                $('.aa-client-brand-slider').append(brands);
                $('.aa-client-brand-slider').slick("unslick");
                jQuery('.aa-client-brand-slider').slick({
                    dots: false,
                    infinite: false,
                    speed: 300,
                    autoplay: true,
                    autoplaySpeed: 2000,
                    slidesToShow: 5,
                    slidesToScroll: 1,
                    responsive: [
                      {
                        breakpoint: 1024,
                        settings: {
                          slidesToShow: 4,
                          slidesToScroll: 4,
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

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.brand();
    }
}


new Brand().main();
