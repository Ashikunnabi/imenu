/*
* =============================================================================
*                                   MY account
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
        $("#your_information").addClass("active");
        let content_height = $(".container-fluid").height() + 100;
        // set sidebar height
        $('#sidebar-wrapper').css('height', content_height + 'px');
    };
    /*
    * =========================================================================
    *                       User edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit user form value setup
        $.ajax({
            url: user_api_url + uuid,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'company_application_document') (value != null) ? $('#editCompanyApplicationDocument').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_store_front') (value != null) ? $('#editCompanyStoreFront').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_commercial_location') (value != null) ? $('#editCompanyCommercialLocation').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_reseller_permit') (value != null) ? $('#editCompanyResellerPermit').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_retail_sales_floor') (value != null) ? $('#editCompanyRetailSalesFloor').attr('href', `/media/${value}`) : "";
                        else if (key === 'is_staff') (value === true) ? $('input[name=is_staff]').click() : "";
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#user_edit_readonly'), response);
                setTimeout(function () {
                    $('input[name=password]').val('')
                }, 1000);

                $(document).on('change', "input[name='password']", function (e) {
                    if ($("input[name='password']").val() !== '') {
                        if ($("input[name='password1']").val() === '') {
                            $("input[name='password1']").attr('required', 'required');
                        }
                    } else {
                        $("input[name='password1']").removeAttr('required');
                        $("form").parsley().reset();
                    }
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
    *                       User edit
    * =========================================================================
    **/

    edit = () => {
        // edit user
        $(document).on('submit', '#user_edit', function (e) {
            e.preventDefault();
            const user_edit_form = $('#user_edit').parsley();
            let user_edit_form_data = new FormData($('#user_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (user_edit_form.isValid()) {
                // make form attributes request friendly
                if (user_edit_form_data.has('email')) user_edit_form_data.delete('email');
                if (user_edit_form_data.has('password')) ($("input[name='password']").val() === '') ? user_edit_form_data.delete('password') : '';
                if (user_edit_form_data.has('password1')) user_edit_form_data.delete('password1');
                if (user_edit_form_data.has('company_application_document')) ($("input[name='company_application_document']").val() === '') ? user_edit_form_data.delete('company_application_document') : '';
                if (user_edit_form_data.has('company_store_front')) ($("input[name='company_store_front']").val() === '') ? user_edit_form_data.delete('company_store_front') : '';
                if (user_edit_form_data.has('company_commercial_location')) ($("input[name='company_commercial_location']").val() === '') ? user_edit_form_data.delete('company_commercial_location') : '';
                if (user_edit_form_data.has('company_reseller_permit')) ($("input[name='company_reseller_permit']").val() === '') ? user_edit_form_data.delete('company_reseller_permit') : '';
                if (user_edit_form_data.has('company_retail_sales_floor')) ($("input[name='company_retail_sales_floor']").val() === '') ? user_edit_form_data.delete('company_retail_sales_floor') : '';
                if (!user_edit_form_data.has('is_staff')) user_edit_form_data.append('is_staff', 0);
                user_edit_form_data.append('is_active', 1);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: update_own_profile_info_api_url,
                    headers: {"X-CSRFToken": csrf_token},
                    type: "PATCH",
                    data: user_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.reload();
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
        this.edit_form_value_set();
        this.edit();
    }
}


new MyAccount().main();
