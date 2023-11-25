/*
* =============================================================================
*                                   CAROUSEL
* =============================================================================
**/

class Carousel {

    /*
    * =========================================================================
    *                       Carousel in home page
    * =========================================================================
    **/
    carousel_template = (title, description, image_url, discount, redirect_url) => {
        return `        
            <li>
                <div class="seq-model">
                    <!--                <img data-seq src="img/slider/1.jpg" alt="Men slide img" />-->
                    <img data-seq
                         src="${image_url}"
                         alt="Men slide img"/>
                </div>
                <div class="seq-title">
                    ${discount > 0 ? `<span data-seq>Save Up to ${discount}% Off</span>` : ''}
                    ${title !== '' ? `<h2 data-seq>${title}</h2>` : ''}
                    ${description !== '' ? `<p data-seq>${description}</p>` : ''}
                    ${redirect_url !== '' ? `<a data-seq href="${redirect_url}" class="aa-shop-now-btn aa-secondary-btn">SHOP NOW</a>` : ''}
                </div>
            </li>
        `
    };

    carousel = () => {
        let self = this;
        $.ajax({
            url: carousel_api_url,
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    $('.seq-canvas').append(
                        self.carousel_template(
                            value.title,
                            value.description,
                            '/media/'+value.image,
                            value.discount,
                            value.redirect_url)
                    );
                });
                // Get the Sequence element
                var sequenceElement = document.getElementById("sequence");

                // Place your Sequence options here to override defaults
                // See: http://sequencejs.com/documentation/#options
                var options = {
                  animateCanvas: false,
                  phaseThreshold: false,
                  preloader: true,
                  reverseWhenNavigatingBackwards: true
                };

                // Launch Sequence on the element, and with the options we specified above
                sequence(sequenceElement, options);
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
        this.carousel();
    }
}


new Carousel().main();
