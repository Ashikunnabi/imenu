/*
* =============================================================================
*                                   NAV CATEGORY
* =============================================================================
**/

class NavCategory {

    categories = () => {
        let self = this;
        $.ajax({
            url: nav_category_api_url,
            type: "GET",
            success: function (resp) {
                let parent_categories = [];
                // rearrange response
                $.map(resp.data, function (value, index) {
                    if (value.parent === null) {
                        value.children = [];
                        parent_categories.push(value);
                    }
                });
                $.map(resp.data, function (value, index) {
                    if (value.parent !== null) {
                        $.map(parent_categories, function (parent, index) {
                            if (parent.id === value.parent) {
                                parent.children.push(value);
                            }
                        })
                    }
                });
                // set categories at home page
                let html = '';
                $.map(parent_categories, function (value, index) {
                    let url = value.redirect_url !== '#' ? value.redirect_url : 'javascript:;';
                    let new_tab = value.redirect_url !== '#'
                        ? value.redirect_url.indexOf('https://gisdealers.com/') > -1 ? '' : 'target="_blank"'
                        : '';
                    html += `                    
                        <li>
                            <a href="${url}" ${new_tab}>${value.title} 
                                ${(value.children.length > 0) ? '<span class="caret"></span>': ''}                                
                            </a>
                            ${(value.children.length > 0) ? `<ul id=nav_cat_${value.hashed_id} class="dropdown-menu"></ul>` : ''}
                        </li>
                    `;
                });
                $('.navbar-nav').append(html);

                $.map(parent_categories, function (value, index) {
                    let children = '';
                    if (value.children.length > 0) {
                        $.map(value.children, function (value, index) {
                            let url = value.redirect_url !== '#' ? value.redirect_url : 'javascript:;';
                            let new_tab = value.redirect_url !== '#'
                                ? value.redirect_url.indexOf('https://1120distributingportal.com/') > -1 ? '' : 'target="_blank"'
                                : '';
                            children += `<li><a href="${url}" ${new_tab}">${value.title}</a></li>`
                        });
                        $(`#nav_cat_${value.hashed_id}`).append(children);
                    }
                });
                $('.navbar-nav').smartmenus('refresh');
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


new NavCategory().main();
