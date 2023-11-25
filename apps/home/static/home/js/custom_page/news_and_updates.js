/*
* =============================================================================
*                                   NEWS AND UPDATES
* =============================================================================
**/

class NewsAndUpdates {

    // FOR ROUNDROLL
//     news_and_updates = () => {
//         let self = this;
//         $.ajax({
//             url: flyer_api_url,
//             type: "GET",
//             success: function (resp) {
//                 $.map(resp.data, function (value, index) {
//                     let data = `
//                         <a target="_blank" rel="rondell" href="/media/${value.image}" title="${value.title}">
//                             <img src="/media/${value.image}" alt="${value.title}" title="${value.title}">
//                             <h5>${value.title}</h5>
// <!--                            <p></p>-->
//                         </a>
//                     `;
//                     $('#rondellCarousel').append(data);
//                 });
//
//                 // Create a rondell with the 'carousel' preset and set an option
//                 // to disable the rondell while the lightbox is displayed
//                 $("#rondellCarousel > *").rondell({
//                   preset: "carousel"
//                 })
//             },
//             error: function (response) {
//                 console.log(response)
//             }
//         });
//     };

    news_and_updates = () => {
        let self = this;
        $.ajax({
            url: flyer_api_url + '?promotional=0',
            type: "GET",
            success: function (resp) {
                let flyers = [];
                $.map(resp.data, function (value, index) {
                    flyers.push(
                        ` 
                        <div class="col-md-4 col-sm-4">
                            <div class="aa-latest-blog-single">
                                <figure class="aa-blog-img">
                                    <a href="#" data-toggle="modal" data-target="#largeModal_${value.hashed_id}"><img
                                            src="/media/${value.image}"
                                            alt="${value.title}" id="f_image_${value.hashed_id}"></a>
<!--                                    <figcaption class="aa-blog-img-caption">-->
<!--                                        <span href="#"><i-->
<!--                                                class="fa fa-eye"></i>5K</span>-->
<!--                                        <a href="#"><i-->
<!--                                                class="fa fa-thumbs-o-up"></i>426</a>-->
<!--                                        <a href="#"><i-->
<!--                                                class="fa fa-comment-o"></i>20</a>-->
<!--                                        <span href="#"><i-->
<!--                                                class="fa fa-clock-o"></i>June 26, 2016</span>-->
<!--                                    </figcaption>-->
                                </figure>
                                <div class="aa-blog-info">
                                    <h3 class="aa-blog-title"><a href="${value.redirect_url}">${value.title}</a></h3>
<!--                                    <p>Lorem ipsum dolor sit amet, consectetur-->
<!--                                        adipisicing elit. Assumenda, ad? Autem-->
<!--                                        quos natus nisi-->
<!--                                        aperiam, beatae, fugiat odit vel-->
<!--                                        impedit dicta enim repellendus animi.-->
<!--                                        Expedita quas reprehenderit-->
<!--                                        incidunt, voluptates corporis.</p>-->
<!--                                    <a href="#" class="aa-read-mor-btn">Read-->
<!--                                        more <span-->
<!--                                                class="fa fa-long-arrow-right"></span></a>-->
                                </div>
                            </div>
                        </div>
                                                
                        <!-- The Modal -->
                        <div class="modal fade" id="largeModal_${value.hashed_id}" tabindex="-1" role="dialog" aria-labelledby="basicModal" aria-hidden="true">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content flyer-modal-content">
                                    <div class="modal-header">
                                        <a href="${value.redirect_url}" target="_blank">${value.title} <i class="fa fa-external-link" aria-hidden="true"></i></a>
                                        <button type="button" class="btn btn-default" data-dismiss="modal" style="float: right">Close</button>
                                    </div>
                                    <div class="modal-body flyer-modal-body">
                                        <!-- carousel -->
                                        <div
                                            id='carouselExampleIndicators_${value.hashed_id}'
                                            class='carousel slide'
                                            data-ride='carousel'
                                        >
                                            <ol class='carousel-indicators'>
                                                ${self.imageIndicator(value)}
                                                <!--<li data-target='#carouselExampleIndicators_${value.hashed_id}' data-slide-to='0' class='active'></li>
                                                <li data-target='#carouselExampleIndicators_${value.hashed_id}' data-slide-to='1'></li>
                                                <li data-target='#carouselExampleIndicators_${value.hashed_id}' data-slide-to='2'></li>-->
                                            </ol>
                                            <div class='carousel-inner'>
                                                ${self.image(value)}
                                                <!--<div class='item active'>
                                                    <img class='img-size' src='/media/${value.image}' alt='First slide' />
                                                </div>
                                                <div class='item'>
                                                    <img class='img-size' src='/media/${value.image}' alt='Second slide' />
                                                </div>
                                                <div class='item'>
                                                    <img class='img-size' src='/media/${value.image}' alt='Third slide' />
                                                </div>-->
                                            </div>
                                            <a class='carousel-control-prev' href='#carouselExampleIndicators_${value.hashed_id}' role='button' data-slide='prev'>
                                                <span class='carousel-control-prev-icon' aria-hidden='true'></span>
                                                <span class='sr-only'>Previous</span>
                                            </a>
                                            <a class='carousel-control-next' href='#carouselExampleIndicators_${value.hashed_id}' role='button' data-slide='next'>
                                                <span class='carousel-control-next-icon' aria-hidden='true'></span>
                                                <span class='sr-only'>Next</span>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`
                    );

                });
                $('#aa-latest-flyer-area').append(flyers);
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    imageIndicator = (flyer) => {
        let indicator = '';
        if (flyer.image) {
            indicator = `<li data-target='#carouselExampleIndicators_${flyer.hashed_id}' data-slide-to='0' class='active'></li>`;
        }
        if (flyer.image1) {
            indicator += `<li data-target='#carouselExampleIndicators_${flyer.hashed_id}' data-slide-to='1'></li>`;
        }
        if (flyer.image2) {
            indicator += `<li data-target='#carouselExampleIndicators_${flyer.hashed_id}' data-slide-to='2'></li>`;
        }
        if (flyer.image3) {
            indicator += `<li data-target='#carouselExampleIndicators_${flyer.hashed_id}' data-slide-to='3'></li>`;
        }
        return indicator;
    };

    image = (flyer) => {
        let image = '';
        if (flyer.image) {
            image = `
                <div class='item active'>
                    <img class='img-size' src='/media/${flyer.image}' alt='First slide' />
                </div>`;
        }
        if (flyer.image1) {
            image += `
                <div class='item'>
                    <img class='img-size' src='/media/${flyer.image1}' alt='First slide' />
                </div>`;
        }
        if (flyer.image2) {
            image += `
                <div class='item'>
                    <img class='img-size' src='/media/${flyer.image2}' alt='First slide' />
                </div>`;
        }
        if (flyer.image3) {
            image += `
                <div class='item'>
                    <img class='img-size' src='/media/${flyer.image3}' alt='First slide' />
                </div>`;
        }
        return image;
    };

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.news_and_updates();
    }
}


new NewsAndUpdates().main();
