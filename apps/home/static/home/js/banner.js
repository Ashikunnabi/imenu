/*
* =============================================================================
*                                   BANNER
* =============================================================================
**/

class Banner {

    banner = () => {
        let self = this;
        $.ajax({
            url: banner_api_url,
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    if (value.human_readable_page === 'Home page') {
                        let banner = `.aa-banner_${value.order}`;
                        $(banner).show();
                        $(banner + ' .aa-banner-area a').attr('href', value.redirect_url);
                        $(banner + ' .aa-banner-area a img').attr('src', "/media/" + value.image);

                        if (value.order === 3) {
                            let banner = `.two_banner_row`;
                            $('#col_2').parent().parent().removeClass('col-md-12').addClass('col-md-6');
                            $('#col_1').show();
                            $(banner).show().css('display', 'inline-block').css('width', '100%');
                            $(banner + ' .aa-banner-area #col_1').attr('href', value.redirect_url);
                            $(banner + ' .aa-banner-area #col_1 img').attr('src', "/media/" + value.image);
                        }
                        if (value.order === 4) {
                            let banner = `.two_banner_row`;
                            $('#col_1').parent().parent().removeClass('col-md-12').addClass('col-md-6');
                            $('#col_2').show();
                            $(banner).show().css('display', 'inline-block').css('width', '100%');
                            $(banner + ' .aa-banner-area #col_2').attr('href', value.redirect_url);
                            $(banner + ' .aa-banner-area #col_2 img').attr('src', "/media/" + value.image);
                        }
                    }
                })
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
        this.banner();
    }
}


new Banner().main();
