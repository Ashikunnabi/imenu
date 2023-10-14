// Module 1: categoryModule.js
export const categoryModule = (function () {
    // Private variables and functions

    function categoryHTML(category) {
        let html = `
        <div class="col-4 text-center">
            <a href="/category/${category.uuid}/product-list">
                <div class="dz-media media-60">
                    <img src="${category.document_thumbnail || "/static/front_end/assets/images/categore/5.png"}" alt="image">
                </div>
                <span>${category.name}</span>
            </a>	
        </div>
        `
        return html
    }

    function getCategories(is_pinned=0) {
        $.ajax({
            url: `/api/v1/menus/?is_pinned=${is_pinned}`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                // Handle the successful response here
                let parent_component = "catagore-bx"
                $.map(data.data, function (v, i) {
                    $(document).find(`.${parent_component}`).append(
                        categoryHTML(v)
                    )
                })
            },
            error: function (xhr, status, error) {
                // Handle errors here
                console.error("AJAX request failed:", status, error);
            }
        });

    }

    // Public methods
    return {
        getCategories: getCategories,
    };
})();
