/*
* =============================================================================
*                                   BANNER
* =============================================================================
**/

class BrandList {

    banner = () => {
        let self = this;
        $.ajax({
            url: brand_api_url,
            type: "GET",
            success: function (resp) {
                $.map(resp.data, function (value, index) {
                    let image_url = value.image ? '/media/' + value.image : '/static/base/img/no_image.png';
                    let price_sheet_url = value.price_sheet_for_dealer ? '/media/' + value.price_sheet_for_dealer : '';
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
                    let brand_old = `
                        <div class="card 1 ln-${ln}" onclick="location.href='/product-list/?brand=${value.hashed_id}'">
                          <div class="card_image"> <img src="${image_url}" /> </div>
                          <div class="card_title title-white">
                            <p><span style="background-color: #ff6666">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${value.name}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
                          </div>
                        </div>
                    `;

                    let download_price_sheet = (price_sheet_url !== '') ?`
                            <a style="background-color:#337ab7;margin:30px;padding:10px;position:absolute;z-index:1;border-radius:0 0 10px 10px"
                                href="${price_sheet_url}"
                                title="Export/Download Price Sheet"
                                download=""
                            >
                                <i class="fa fa-download" style="color:white" aria-hidden="true"></i>
                            </a>`: "" ;

                    let brand = `
                        <div style="display: flex"  class="1 ln-${ln}">
                            ${download_price_sheet}
                            <div class="card" onclick="location.href='/product-list/?brand=${value.hashed_id}'">
                              <div class="card_image"> <img src="${image_url}" /> </div>
                              <div class="card_title title-white">
                                <p><span style="background-color: #ff6666">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${value.name}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
                              </div>
                            </div>
                        </div>
                    `;
                    $('#brands_list').append(brand)
                });

                $('#brands_list').listnav({
                    filterSelector: '.last-name',
                    includeNums: true,
                    noMatchText: `
                        <div class="card 1">
                          <div class="card_image"> <img src="https://media.giphy.com/media/10SvWCbt1ytWCc/giphy.gif" /> </div>
                          <div class="card_title title-white">
                            <p><span style="background-color: #ff6666">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nothing found&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
                          </div>
                        </div>
                    `
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
        this.banner();
    }
}


new BrandList().main();
