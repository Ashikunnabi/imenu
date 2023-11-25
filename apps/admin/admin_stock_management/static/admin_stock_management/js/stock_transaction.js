/*
* =============================================================================
*                             STOCK TRANSACTION
* =============================================================================
**/

class stockTransaction {
    myChart = null

    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_stock_management_a').click();
        $('#sidebar_option_stock_management_stock_transaction').addClass('active');
    };


    /*
    * =========================================================================
    *                      STOCK TRANSACTIONs in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#stockTransactionDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B><"toolbar">flrtip',
            "buttons": [
                {
                    extend: 'copy',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'pdf',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'excel',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'csv',
                    exportOptions: {orthogonal: 'export'}
                },
                {
                    extend: 'print',
                    exportOptions: {orthogonal: 'export'}
                },
                // {
                //     extend: 'print',
                //     title: 'USERS',
                //     messageTop: '<h5 class="text-center">User List</h5>',
                //     messageBottom: null
                // }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': stock_transaction_api_url,
                'type': 'GET',
                'complete': function (res) {
                    self.pie_chart(
                        $.map(res.responseJSON.kwargs.count_product, function (v, i) { return v.product__product_id }),
                        $.map(res.responseJSON.kwargs.count_product, function (v, i) { return v.product__product_id__count })
                    )

                    $("#aggr_purchase").text(res.responseJSON.kwargs.prices.purchase)
                    $("#aggr_sell").text(res.responseJSON.kwargs.prices.sell)
                },
                'error': function (x, status, error) {
                    notify(error, 'error', 3000);
                },
            },
            "rowCallback": function (row, data, displayNum, displayIndex, dataIndex) {
                // $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Date", "data": "created_at" },
                { "title": "Ref", "data": "" },
                { "title": "SKU", "data": "" },
                { "title": "Stock", "data": "previous_stock" },
                { "title": "Unit Price", "data": "previous_unit_price" },
                { "title": "Amount", "data": "previous_amount" },
                { "title": "Stock", "data": "purchase_stock" },
                { "title": "Unit Price", "data": "purchase_unit_price" },
                { "title": "Amount", "data": "purchase_amount" },
                { "title": "Stock", "data": "sell_stock" },
                { "title": "Unit Price", "data": "sell_unit_price" },
                { "title": "Amount", "data": "sell_amount" },
                { "title": "Stock", "data": "current_stock" },
                { "title": "Unit Price", "data": "current_unit_price" },
                { "title": "Amount", "data": "current_amount" },
                // {"title": "Discount", "data": ""},
                { "title": "Delivery Cost", "data": "delivery_cost" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    "targets": [1],
                    "visible": true,
                    "searchable": true,
                    "orderablr": true,
                    "render": function (data, type, row, meta) {
                        return moment(row.created_at).format('ll');
                    },
                },
                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let html = ''
                        html += `<a href="${row.transaction_type_details.url}" target="_blank">${row.transaction_type_details.number}</a>`
                        return html;
                    },
                },
                {
                    "targets": [3],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let html = ''
                        html += `<a href="${row.product_details.url}" target="_blank">${row.product_details.product_id}</a>`
                        return html;
                    },
                },
                // {
                //     "targets": [16],
                //     "visible": true,
                //     "searchable": true,
                //     "render": function (data, type, row, meta) {
                //         let html = `${row.discount_percentage}% / $${row.discount}`
                //         return html;
                //     },
                // },
            ],
        });

        // Single click row select the row and mark a different color
        $('#stockTransactionDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        // $('#stockTransactionDataTable tbody').on('dblclick', 'tr', function () {
        //     let data = table.row(this).data();
        //     window.location = 'edit/' + data.uuid;
        // });

        $('#stockTransactionDataTable thead').prepend(`            
            <tr style="text-align:center">
                <th colspan="4"></th>
                <th colspan="3">Previous</th>
                <th colspan="3">Pruchase</th>
                <th colspan="3">Sell</th>
                <th colspan="3">Current</th>
            </tr>
        `)

        $('#stockTransactionDataTable').append(`
            <tfoot>
                <tr style="text-align:center">
                    <th colspan="9"></th>
                    <th id="aggr_purchase">00.00</th>
                    <th colspan="2"></th>
                    <th id="aggr_sell">00.00</th>
                    <th colspan="4"></th>
                </tr>
            </tfoot>
        `)
        self.filter_datatable(table);
    };


    table_row = `<tr>
                    <td><select class="product" style="width:200px;height:25px">
                    <option value="" selected="selected">Search Part No</option>
                    </select></td>
                    <td><input class="packing" type="number" value=""></td>
                    <td><input class="quantity" type="number" value="0"></td>
                    <td><input class="received" type="number" value="0"></td>
                    <td><input class="pending" type="number" value="0"></td>
                    <td><input class="price" type="number" value="0"></td>
                    <td><input class="subtotal" type="number" value="0"></td>
                    <td class="remove_row">&nbsp;&nbsp;&nbsp;&nbsp;-</td>
                </tr>`


    /*
    * =========================================================================
    *                      LOGO ATTACHMENT
    * =========================================================================
    **/

    showPreview = () => {
        $(document).on('change', '#logo-button', function (event) {
            if (event.target.files.length > 0) {
                var reader = new window.FileReader();
                reader.readAsDataURL(event.target.files[0]);
                reader.onloadend = function () {
                    var src = reader.result;
                    var preview = document.getElementById("logo-preview");
                    preview.src = src;
                    preview.style.display = "block";
                }
            }
        });
    }


    /*
    * =========================================================================
    *                      INITIAL TABLE
    * =========================================================================
    **/
    initial_table = () => {
        let self = this
        $('#po_number').val(`PO${parseInt((new Date()).getTime() / 1000)}`)
        $('.section5 table tbody').append(self.table_row)
    }


    /*
    * =========================================================================
    *                      CALCULATE PRICE
    * =========================================================================
    **/
    calculatePrice = () => {
        let self = this
        $(document).on('change keyup', '.packing, .quantity, .price', function (e) {
            let tr = $(this).parent().parent()
            let packing = parseFloat(tr.find('.packing').val()) || 0
            let quantity = parseFloat(tr.find('.quantity').val()) || 0
            let price = parseFloat(tr.find('.price').val()) || 0

            if (quantity === '' || price === '') {
                tr.find('.subtotal').val(0)
            } else {
                tr.find('.subtotal').val((packing + (quantity * price)).toFixed(2))
                self.calculateTotal()
            }
        })
    }

    calculateTotal = () => {
        let total = 0,
            sub_total = 0,
            discount_percentage = 0,
            discount = 0

        const myPromise = new Promise((resolve, reject) => {
            $.each($('.subtotal'), function (i, v) {
                sub_total += parseFloat($(v).val())
                $('#sub_total').html(sub_total.toFixed(2))
                $('#total').html(sub_total.toFixed(2))
                total = sub_total
                if (i == $('.subtotal').length - 1) {
                    resolve()
                }
            })
        });

        myPromise
            .then(
                () => {
                    discount_percentage = $('#discount_percentage').val()
                    discount = (discount_percentage * sub_total) / 100
                    total = sub_total - discount
                    $('#discount').html(discount.toFixed(2))
                    $('#total').html(total.toFixed(2))
                },
                () => { }
            )


        $(document).on('change keyup', '#discount_percentage', function (e) {
            discount_percentage = $(this).val()
            discount = (discount_percentage * sub_total) / 100
            total = sub_total - discount
            $('#discount').html(discount.toFixed(2))
            $('#total').html(total.toFixed(2))
        })
    }


    /*
    * =========================================================================
    *                      PRODUCT GET SET
    * =========================================================================
    **/
    get_product = () => {
        $('.product').select2({
            minimumInputLength: 3,
            ajax: {
                url: '/api/v1/product/search/',
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.id,
                            text: v.product_id,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });
    }

    set_product = () => {
        let self = this
        $(document).on('change', '.product', function (e) {
            let data = $(this).select2('data')[0].other
            let tr = $(this).parent().parent()

            // set description
            tr.find('textarea').val(data.description).change()
            // set quantity
            tr.find('.quantity').val(1)
            // set price
            tr.find('.price').val(parseFloat(data.jobbar_price).toFixed(2)).trigger('change')
            self.calculateTotal()
        })
    }


    /*
    * =========================================================================
    *                      ADD ROW
    * =========================================================================
    **/
    add_new_row = () => {
        let self = this

        $('.add_new_item').on('click', function (e) {
            $('.section5 table tbody').append(self.table_row)
            self.get_product()

        });
    }


    /*
    * =========================================================================
    *                      REMOVE ROW 
    * =========================================================================
    **/
    remove_existing_row = () => {
        let self = this

        $(document).on('click', '.remove_row', function (e) {
            $(this).closest("tr").remove();
            self.calculateTotal()
        });
    }


    /*
    * =========================================================================
    *                      SUPPLIER GET SET
    * =========================================================================
    **/
    get_supplier = () => {
        $('#supplier').select2({
            minimumInputLength: 3,
            ajax: {
                url: '/api/v1/brand/search/',
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.id,
                            text: v.name,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });
    }

    set_supplier = () => {
        let self = this
        $(document).on('change', '#supplier', function (e) {
            let data = $(this).select2('data')[0].other
            let p = $(this).parent()

            // set address
            p.find('textarea').val(data.company_address).change()
        })
    }


    /*
    * =========================================================================
    *                      PRINT PREVIEW
    * =========================================================================
    **/
    print_preview = () => {
        $('.print_preview').on('click', function (e) {
            document.title = $('#po_number').val()
            window.print();
        });
    }
    //=========================== /PRINT ======================================


    /*
    * =========================================================================
    *                      SAVE PO
    * =========================================================================
    **/
    save = () => {
        $('.save_po').on('click', function (e) {
            let data = {};
            data.number = $('#po_number').val()
            data.date = $('#date').val()
            data.data = {}
            data.data.image = $('#logo-preview').attr('src')
            data.data.address = $('#address').val()
            data.data.url = $('#url').val()
            data.data.po_number = $('#po_number').val()
            data.data.order_date = $('#date').val()
            data.data.est_receive_date = $('#est_receive_date').val()
            data.data.requested_shipping = $('#requested_shipping').val()
            data.data.carrier_shipping = $('#carrier_shipping').val()
            data.data.supplier = {}
            data.data.supplier.name = $('#supplier').select2('data')[0].text
            data.data.supplier.id = $('#supplier').val()
            data.data.supplier.address = $('#supplier_address').val()
            data.data.bill_to = $('#bill_to').val()
            data.data.ship_to = $('#ship_to').val()
            data.data.sub_total = $('#sub_total').text()
            data.data.discount_percentage = $('#discount_percentage').val()
            data.data.discount = $('#discount').text()
            data.data.total = $('#total').text()
            data.data.additional_notes = $('#additional_notes').val()
            data.data.products = []

            $('#products').find('tr').each(function (i, el) {
                data.data.products.push({
                    id: $(this).find('.product').val(),
                    product_id: $(this).find('.product').select2('data')[0].text,
                    description: $(this).find('.description').val(),
                    packing: $(this).find('.packing').val(),
                    quantity: $(this).find('.quantity').val(),
                    price: $(this).find('.price').val(),
                    subtotal: $(this).find('.subtotal').val(),
                })
            });

            // add url
            let url = po_api_url,
                type = "POST"
            // edit url
            if (page === 'edit') {
                url = po_api_url + uuid + '/'
                type = "PATCH"
            }

            $.ajax({
                url: url,
                type: type,
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify('Success', 'success', 3000);
                    if (page === 'add') {
                        setTimeout(() => { window.location.href = po_list_url; }, 4000);
                    }
                },
                error: function (response) {
                    if (response.status === 422) {
                        $.map(response.responseJSON.details, function (v, i) {
                            $.each(v, function (j, k) {
                                notify(k, 'error', 2000);
                            })
                        });
                    }
                }
            });
        });
    }


    /*
    * =========================================================================
    *                       EDIT PAGE DATA SET 
    * =========================================================================
    **/
    edit_page_data_set = () => {
        let self = this
        $.ajax({
            url: po_api_url + uuid + '/',
            type: "GET",
            success: function (resp) {
                let data = resp.data

                $('#po_number').val(data.po_number)
                $('#date').val(data.order_date)
                $('#logo-preview').attr('src', data.image)
                $('#address').val(data.address)
                $('#url').val(data.url)
                $('#est_receive_date').val(data.est_receive_date)
                $('#requested_shipping').val(data.requested_shipping)
                $('#carrier_shipping').val(data.carrier_shipping)


                // modify the added option manually - add extra data attributes (in addition to id and text)
                // $('#supplier').empty().append(
                //     `<option value="${data.supplier.id}">${data.supplier.name}</option>`
                // )

                // let $current_option_data = $('#supplier').select2('data').find(function (currentOption) {
                //     return currentOption.id == data.supplier.id
                // });

                // if ($current_option_data) {
                //     $current_option_data['other'] = {'company_address': data.supplier.address};
                // }


                $('#supplier_address').val(data.supplier.address)
                $('#ship_to').val(data.ship_to)
                $('#bill_to').val(data.bill_to)
                $('#sub_total').text(data.sub_total)
                $('#discount_percentage').val(data.discount_percentage)
                $('#discount').text(data.discount)
                $('#total').text(data.total)
                $('#additional_notes').val(data.additional_notes)
                let rows = ''
                $.each(data.products, function (i, v) {
                    rows += `<tr>
                        <td><select class="product" style="width:200px;height:25px">
                        <option value="${v.id}" selected="selected">${v.product_id}</option>
                        </select></td>
                        <td><input class="packing" type="number" value="${v.packing}"></td>
                        <td><input class="quantity" type="number" value="${v.quantity}"></td>
                        <td><input class="received" type="number" value="${v.received}"></td>
                        <td><input class="pending" type="number" value="${v.pending}"></td>
                        <td><input class="price" type="number" value="${v.price}"></td>
                        <td><input class="subtotal" type="number" value="${v.subtotal}"></td>
                        <!--<td class="remove_row">&nbsp;&nbsp;&nbsp;&nbsp;-</td>-->
                        <td 
                            class="update_stock" 
                            data-po="${uuid}"
                            data-pid="${v.id}"
                            data-uuid="${v.uuid}"
                            data-product_id="${v.product_id}"
                            data-quantity="${v.quantity}"
                            data-received="${v.received}"
                            data-pending="${v.pending}"
                            data-unit_price="${v.price}"
                        >&nbsp;&nbsp;&nbsp;&nbsp;<i class='fas fa-cloud-upload-alt'></i></td>
                    </tr>`
                });
                $('#products').empty().append(rows)
                self.get_product()
                $('.description').trigger('change')


                // disable modification as already stock updated and PO is locked
                if (resp.is_locked) {
                    self.disable_edit_page_modification()
                }
            },
            error: function (response) {
                if (response.status === 422) {
                    $.map(response.responseJSON.details, function (v, i) {
                        $.each(v, function (j, k) {
                            notify(k, 'error', 2000);
                        })
                    });
                }
            }
        });
    }


    /*
    * =========================================================================
    *                       EDIT PAGE UPDATE STOCK
    * =========================================================================
    **/
    depricated_update_stock = () => {
        let self = this
        $('.update_stock').on('click', function (e) {
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to UPDATE PO anymore!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, update stock!'
            }).then((result) => {
                if (result.isConfirmed) {
                    let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
                    // do ajax request to update stock and lock PO
                    let data = {
                        is_stock_updated: true,
                        is_locked: true,
                    }
                    $.ajax({
                        url: po_api_url + uuid + '/',
                        headers: { "X-CSRFToken": csrf_token },
                        type: "PATCH",
                        data: JSON.stringify(data),
                        dataType: 'json',
                        contentType: "application/json",
                        success: function (resp) {
                            Swal.fire(
                                'UPDATED & LOCKED!',
                                'Stock has been updated for this PO.',
                                'success'
                            );

                            // disable modification as already stock updated and PO is locked
                            self.disable_edit_page_modification()
                        },
                        error: function (response) {
                            $.map(response.responseJSON.details, function (v, i) {
                                $.each(v, function (j, k) {
                                    notify(k, 'error', 5000);
                                })
                            });
                        }
                    });
                }
            })
        })
    }

    update_stock = () => {
        let self = this
        let selected_product_data = null
        $(document).on('click', '.update_stock', function (e) {
            let data = $(this).data()
            selected_product_data = data

            $('#modal_part_number').val(data.part_number);
            $('#modal_quantity').val(data.quantity);
            $('#modal_received').val(data.received);
            $('#modal_pending').val(data.pending);
            $("#update_stock_modal").modal("show");

            // get product for warehouse 
            $.ajax({
                url: product_api_url + data.uuid + '/',
                type: "GET",
                success: function (resp) {
                    $('#update_stock_modal #warehouse_section').empty()
                    self.modal_warehouse_template(resp.warehouses)
                },
                error: function (response) {
                    $.map(response.responseJSON.details, function (v, i) {
                        $.each(v, function (j, k) {
                            notify(k, 'error', 5000);
                        })
                    });
                }
            });
        })

        $(document).on('click', '#update_stock_submit_button_modal', function (e) {
            let warehouses = []
            let warehouse_list = $('#update_stock_modal #warehouse_section table tbody').find('.warehouse_sub_stock')

            if (parseFloat($('#modal_current_received').val()) < 1) {
                notify('Current received must be greater than 0', 'error', 5000);
                return
            }
            if (warehouse_list.length < 1) {
                notify('At least one warehouse required', 'error', 5000);
                return
            }
            let total_warehouse_stock_added = 0
            let invalid_entry = false
            $.each(warehouse_list, function (i, v) {
                if ($(v).val() !== '0') {
                    total_warehouse_stock_added += parseFloat($(v).val())

                    if (parseFloat($(v).val()) > parseFloat($(v).data('current_stock'))) {
                        invalid_entry = true
                    }
                }
            })
            if (total_warehouse_stock_added < 1) {
                notify('At least one warehouse need stock update', 'error', 5000);
                return
            }
            if (total_warehouse_stock_added != parseFloat($('#modal_current_received').val())) {
                notify("Warehouse must have equal stock in current received", 'error', 5000);
                return
            }
            if (parseFloat($('#modal_current_received').val()) > parseFloat($('#modal_pending').val())) {
                notify("Current received can't have stock more than pending", 'error', 5000);
                return
            }
            if (invalid_entry) {
                notify("Warehouse received can't be more than current stock", 'error', 5000);
                return
            }

            // get warehouses info 
            $.each(warehouse_list, function (i, v) {
                warehouses.push({
                    id: $(v).data().id,
                    uuid: $(v).data().uuid,
                    stock: $(v).val()
                })
            })

            let data = {
                id: selected_product_data.pid,
                part_number: selected_product_data.part_number,
                unit_price: selected_product_data.unit_price,
                current_received: $('#modal_current_received').val(),
                uuid: uuid,
                warehouses: warehouses
            }

            $.ajax({
                url: stock_transaction_api_url,
                type: "POST",
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify(k, 'success', 5000);
                },
                error: function (response) {
                    $.map(response.responseJSON.details, function (v, i) {
                        $.each(v, function (j, k) {
                            notify(k, 'error', 5000);
                        })
                    });
                }
            });
        })
    }

    /*
    * =========================================================================
*                       EDIT PAGE UPDATE STOCK SET WAREHOUSE
    * =========================================================================
    **/
    modal_warehouse_template = (warehouses) => {
        let table = `
            <hr>
            <table style="width:100%">
                <caption style="text-align:center;caption-side:top">Warehouse Details</caption>
                <thead>
                    <tr>
                        <th>Warehouse</th>
                        <th>Current Stock</th>
                        <th>Received Stock</th>
                    </tr>
                </thead>
                
                <tbody>
                    
                </tbody>        
            </table>
        `
        $('#update_stock_modal #warehouse_section').append(table)

        let tbody_trs = ''
        if (warehouses.length === 0) {
            tbody_trs += `
                <tr>
                    <td colspan="3" style="text-align:center">No warehouse found.</td>
                </tr>
            `
        }
        $.each(warehouses, function (i, warehouse) {
            tbody_trs += `
                <tr>
                    <td><input type="text" value="${warehouse.name}" style="width:100%" class="form-control" readonly></td>
                    <td><input type="text" value="${warehouse.stock}" style="width:100%" class="form-control" readonly></td>
                    <td><input 
                        class="warehouse_sub_stock form-control" 
                        value="0" 
                        type="text" 
                        data-id="${warehouse.id}"
                        data-uuid="${warehouse.uuid}"
                        data-current_stock="${warehouse.stock}"
                        style="width:100%" >
                    </td>
                </tr>
            `
        })
        $('#update_stock_modal #warehouse_section table tbody').append(tbody_trs)
    }

    /*
    * =========================================================================
    *                       DISABLE EDIT PAGE MODIFICATION
    * =========================================================================
    **/
    disable_edit_page_modification = () => {
        $('.add_new_item, .save_po, .logo-button-label, .fa-paste').hide()
        // $('.remove_row').off('click')
        $('input').prop('readonly', true)
        $('textarea').prop('readonly', true)
        $('select').prop('disabled', true)
        $('#update_stock_modal #modal_current_received, .warehouse_sub_stock').prop('readonly', false)
    }

    /*
    * =========================================================================
    *                       CONTROL COPY PASTE
    * =========================================================================
    **/
    control_copy_paste = () => {
        $('#copy_ship_to_into_bill_to').on('click', function (e) {
            $('#bill_to').val($('#ship_to').val())
        })
        $('#copy_bill_to_into_ship_to').on('click', function (e) {
            $('#ship_to').val($('#bill_to').val())
        })
    }

    /*
    * =========================================================================
    *                       FILTER DATATABLE
    * =========================================================================
    **/
    filter_datatable = (table) => {
        $('div.toolbar').html(`
            <div style="display:flex;gap:10px;">
                <div>
                    <input class="form-control form-control-sm" name="date_range"> 
                </div>  
                <div>
                    <select class="form-control form-control-sm" name="transaction_type">
                        <option value="0">All Transaction</option>
                        <option value="1">Purchase Order</option>
                        <option value="2">Sales Order</option>
                    </select>
                </div>     
                <div>
                    <input type="button" class="btn-primary form-control form-control-sm" id="dt_custom_search" value="search"> 
                </div>       
            </div>        
        `);

        $('input[name="date_range"]').daterangepicker({
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            },
            "alwaysShowCalendars": true,
            "startDate": "01/01/2020",
            "endDate": moment()
        });

        $(document).on('click', '#dt_custom_search', function (e) {
            let url = `${stock_transaction_api_url}?date_range=${$('input[name="date_range"]').val()}&transaction_type=${$('select[name="transaction_type"]').val()}`
            table.ajax.url(url).load();
        })
    }

    /*
    * =========================================================================
    *                       CHART
    * =========================================================================
    **/
    dynamicColors = () => {
        var r = Math.floor(Math.random() * 255);
        var g = Math.floor(Math.random() * 255);
        var b = Math.floor(Math.random() * 255);
        return "rgb(" + r + "," + g + "," + b + ")";
    }

    pie_chart = (labels, values) => {
        let self = this
        // set aggr prices in table
        if (self.myChart instanceof Chart) {
            self.myChart.destroy();
        }

        let data = {
            labels: labels,
            datasets: [{
                label: 'Stock Transaction',
                data: values,
                backgroundColor: $.map(labels, function (v, i) { return self.dynamicColors() }),
                hoverOffset: 4
            }]
        };

        let ctx = document.getElementById('pie_chart');
        self.myChart = new Chart(ctx, {
            type: 'pie',
            data: data
        });
    }

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.list()
        this.select_sidebar_option()
        // this.showPreview()
        this.initial_table()
        // this.get_product()
        // this.set_product()
        // this.get_supplier()
        // this.set_supplier()
        // this.add_new_row()
        // this.calculatePrice()
        // this.remove_existing_row()
        this.print_preview()
        // this.control_copy_paste()
        // this.save()
        if (page === 'edit') {
            this.edit_page_data_set()
            this.update_stock()
        }

    }
}


new stockTransaction().main();