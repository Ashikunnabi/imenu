/*
* =============================================================================
*                                   MY SALES REPS
* =============================================================================
**/

class MyAccount {

    toggle_sidebar = () => {
        $("#menu-toggle").click(function(e) {
          e.preventDefault();
          $("#wrapper").toggleClass("toggled");
        });

    };

    select_sidebar = () => {
        $("#my_sales_reps").addClass("active");
        let content_height = $(".container-fluid").height() + 100;
        // set sidebar height
        $('#sidebar-wrapper').css('height', content_height + 'px');
    };
    /*
    * =========================================================================
    *                       SALES REPS
    * =========================================================================
    **/

    sales_reps = () => {
        // edit user form value setup
        $.ajax({
            url: sales_reps_api_url + `?user=${uuid}`,
            type: "get",
            success: function (response) {
                if (!response.detail.length) {
                    $('.container-fluid table tbody').append(`
                        <tr>
                            <td colspan="5">No Sales Reps found</td>
                        </tr>                         
                                 
                    `);
                    return;
                }
                $.map(response.detail, function (v, i) {
                    if (!v.selected) {
                        return;
                    }
                    $('.container-fluid table tbody').append(`
                        <tr>
                            <td><img
                                    src="/media/${v.image}">
                            </td>
                            <td>${v.title}</td>
                            <td>${v.name}</td>
                            <td>${v.phone}</td>
                            <td>${v.email}</td>
                        </tr>                    
                    `);
                });
            },
            error: function (response) {
                if (response.status === 422) {
                    let errors = '';
                    $.map(response.responseJSON.details, function (v, i) {
                        $.each(v, function (j, k) {
                            errors += `<li>${i}: ${k}</l1>`;
                        })
                    });
                    let final_error = `<ul>${errors}</ul>`;

                    $('.failed')
                        .html(final_error)
                        .css('display', 'block')
                }
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
        this.toggle_sidebar();
        this.select_sidebar();
        this.sales_reps();
    }
}


new MyAccount().main();
