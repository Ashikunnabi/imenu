/*
* =============================================================================
*                                   BANNER
* =============================================================================
**/

class BrandList {

    banner = () => {
        let self = this;
        $.ajax({
            url: brand_page_api_url,
            type: "GET",
            success: function (resp) {
                if (resp.data.length === 0) {
                    $('#brand_page_list').append(`
                    <div style="height: 50vH">No active page found.</div>
                    `);
                    return;
                }

                $.map(resp.data, function (value, index) {
                    let image_url = value.image ? '/media/' + value.image : '/static/base/img/no_image.png';
                    let brandss = `<br>
                    <li class="ln-${value.name.charAt(0).toLowerCase()}">
                        <img src="${image_url}" width="120" height="120">
                        <a href="/product-list/?brand=${value.hashed_id}">${value.name}</a>
<!--                        <p><span><strong>Rank:</strong>&nbsp;</span><span>Commander<span></span></span></p>-->
<!--                        <p><span><strong>Date of Birth:</strong>&nbsp;</span><span>Oct. 13, 2324<span></span></span></p>-->
<!--                        <p><span><strong>Place of Birth:</strong>&nbsp;</span><span>Copernicus City, Luna<span></span></span></p>-->
                     </li>
                    `;
                    let ln = isNaN(value.name.charAt(0).toLowerCase()) ? value.name.charAt(0).toLowerCase() : '_';
                    let brand = `  
                        <div class="card 1 ln-${ln}" onclick="location.href='/brand-page/?brand=${value.hashed_id}'">
                          <div class="card_image"> <img src="${image_url}" /> </div>
                          <div class="card_title title-white">
                            <p><span style="background-color: #ff6666">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${value.name}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
                          </div>
                        </div>
                    `;
                    $('#brand_page_list').append(brand)
                });

                // $('#brand_page_list').listnav({
                //     filterSelector: '.last-name',
                //     includeNums: true,
                //     noMatchText: `
                //         <div class="card 1">
                //           <div class="card_image"> <img src="https://media.giphy.com/media/10SvWCbt1ytWCc/giphy.gif" /> </div>
                //           <div class="card_title title-white">
                //             <p><span style="background-color: #ff6666">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nothing found&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
                //           </div>
                //         </div>
                //     `
                // });
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


new BrandList().main();
