/*
* =============================================================================
*                                   NOTICE
* =============================================================================
**/

class Notice {

    notices = () => {
        let self = this;
        $.ajax({
            url: notice_category_api_url,
            type: "GET",
            success: function (resp) {
                let general_notice = [];
                // rearrange response
                $.map(resp.data, function (value, index) {
                    let redirect_url = value.redirect_url ? value.redirect_url : 'javascript:;';
                    let target = value.target ? value.target : '_self';
                    let background_color = value.background_color ? value.background_color : 'white';
                    let color = value.color ? value.color : 'black';
                    let title = value.title;
                    let data = `
                        <i class="fa fa-dot-circle-o" aria-hidden="true" style="color: #ff6666;"></i>
                        <a href="${redirect_url}" target="${target}" style="background-color: ${background_color}; color: ${color}; padding: 5px;">${title}</a>
                        `;
                    general_notice.push(data);
                });
                $('#general_notice .container .marquee span').append(general_notice)
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
        this.notices();
    }
}


new Notice().main();
