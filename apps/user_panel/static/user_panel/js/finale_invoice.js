/*
* =============================================================================
*                                   Finale Invoice
* =============================================================================
**/

class FinaleInvoice {

    toggle_sidebar = () => {
        $("#menu-toggle").click(function (e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
        });

    };

    select_sidebar = () => {
        $("#finale_invoice").addClass("active");
        setInterval(function (e) {
            let content_height = $(".container-fluid").height();
            // set sidebar height
            $('#sidebar-wrapper').css('height', content_height + 'px');
        }, 2000)

    };

    /*
    * =========================================================================
    *                       Invoice list
    * =========================================================================
    **/

    invoice_list = () => {
        let self = this;
        $.ajax({
            url: finale_invoice_api_url,
            type: "GET",
            success: function (response) {
                if (response.data.length < 1){
                    $('#empty_orders').show();
                    $('.finale-invoice-view-table').hide();
                    return;
                }
                $.each(response.data, function (key, value) {
                    let tracking_number = value.tracking_number !== null ? value.tracking_number : '';
                    let orders_cancellations = `
                        <tr>
                            <td>${key+1}</td>
                            <td class="order_date_time">
                                <span class="day">${moment(value.created_at).format('dddd')}</span>
                                <span class="date">${moment(value.created_at).format('Do')}</span>
                                <span class="month_year">${moment(value.created_at).format('MMM, YYYY')}</span>
                                <span class="time">at ${moment(value.created_at).format('h:mm:ss a')}</span>                                    
                            </td>
                            <td>
                                <a href="/media/${value.invoice}" target="_blank">Download</a><br>
                                 <small><strong>Tracking Number:</strong>${tracking_number}</small>            
                            </td>
                        </tr>
                    `;
                    $('#invoices').append(orders_cancellations);
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
        let self = this;
        self.toggle_sidebar();
        self.select_sidebar();
        self.invoice_list();
    }
}


new FinaleInvoice().main();
