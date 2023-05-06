/*
* =============================================================================
*                             PURCHASE ORDER
* =============================================================================
**/

class PurchaseOrder {
    executed = 0
    edit_data = {}

    /*
    * =========================================================================
    *                      Purchase Orders in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#purchaseOrderDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B><"extra_btn">flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add PO',
                        id: 'addPOButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = po_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete PO',
                        id: 'deletePOButton',
                        class: 'btn btn-danger'
                    },
                    action: function (e, dt, node, config) {
                        let data = dt.rows(".selected").data();
                        // no table row selected
                        if (data[0] === undefined) {
                            notify('Please select an item', 'error');
                            return;
                        }
                        // table row selected so do further actions
                        Swal.fire({
                            title: 'Are you sure?',
                            text: "You won't be able to revert this!",
                            icon: 'warning',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes, delete it!'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
                                // do ajax request to delete
                                $.ajax({
                                    url: po_api_url + data[0].uuid + '/',
                                    headers: {"X-CSRFToken": csrf_token},
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'PO has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        $.map(response.responseJSON.details, function (v, i) {
                                            $.each(v, function (j, k) {
                                                notify(k, 'error', 3000);
                                            })
                                        });
                                    }
                                });
                            }
                        })
                    }
                },
                'copy',
                'excel',
                'pdf',
                'csv',
                'print',
                // {
                //     extend: 'print',
                //     title: 'USERS',
                //     messageTop: '<h5 class="text-center">User List</h5>',
                //     messageBottom: null
                // }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': po_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    notify(error, 'error', 3000);
                    console.log(x, status, error)
                },
            },
            "rowCallback": function(row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                {"title": "SL", "data": ""},
                {"title": "PO Number", "data": "number"},
                {"title": "Created At", "data": "created_at"},
                {"title": "Ordered At", "data": "date"},
                {"title": "Due Date", "data": "due_date"},
                {"title": "Stock Updated/Locked", "data": ""},
                {"title": "Note", "data": "notes"},
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return `${moment(data).format('YYYY-MM-DD')}`;
                    },
                },
                {
                    "targets": [5],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let updated = 'Yes'
                        let locked = 'Yes'
                        if (!row.is_stock_updated) {
                            updated = 'No'
                        }
                        if (!row.is_locked) {
                            locked = 'No'
                        }
                        return `${updated}/${locked}`;
                    },
                },
            ],
        });

        // add extra inputs for additional filtering
        $("div.extra_btn").html(`
            <div class="row">
                <div class="col-md-12">
                
                    <div class="form-group">
                    
                        <div class="custom-control custom-checkbox" style="display: inline-block; margin-left: 5px">
                            <input type="checkbox" class="custom-control-input"
                                   id="is_locked_extra_btn" name="is_locked_extra_btn">
                            <label class="custom-control-label"
                                   for="is_locked_extra_btn">Locked</label>
                        </div>
                    
                        <div class="custom-control custom-checkbox" style="display: inline-block; margin-left: 5px">
                            <input type="checkbox" class="custom-control-input"
                                   id="is_unlocked_extra_btn" name="is_unlocked_extra_btn">
                            <label class="custom-control-label"
                                   for="is_unlocked_extra_btn">Unlocked</label>
                        </div>
                        
                    </div>                    
                </div>
            </div>
        `);

        // additional filter based on extra button
        $(document).on('change', '.custom-control-input, .custom-control-input_date_range', function (e) {
            let url = po_api_url;

            $(`#is_locked_extra_btn`).prop('checked', false);
            $(`#is_unlocked_extra_btn`).prop('checked', false);
            $(`#${$(this).attr('id')}`).prop('checked', true);

            if ($(`#is_locked_extra_btn`).is(':checked')) {
                url += '?is_locked=1';
            }

            if ($(`#is_unlocked_extra_btn`).is(':checked')) {
                url += '?is_locked=0';
            }
            
            url += `?date_range=${$('input[name="date_range"]').val()}`

            table.ajax.url( url ).load();
        });

        // Single click row select the row and mark a different color
        $('#purchaseOrderDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#purchaseOrderDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });

        self.filter_datatable(table);
    };


    table_row = `<tr>
                    <td><select class="product" style="width:200px;height:25px">
                    <option value="" selected="selected">Search Part No</option>
                    </select></td>
                    <td><textarea rows="1" class="description"
                        onkeyup="$(this).css('height', 'auto').css('height', this.scrollHeight + this.offsetHeight - this.clientHeight);"
                        onchange="$(this).css('height', 'auto').css('height', this.scrollHeight + this.offsetHeight - this.clientHeight);"
                    ></textarea></td>
                    <td><input class="packing" type="number" value=""></td>
                    <td><input class="quantity" type="number" value="0"></td>
                    <td><input class="price" type="number" value="0"></td>
                    <td><input class="subtotal" type="number" value="0"></td>
                    <td class="remove_row">&nbsp;&nbsp;&nbsp;&nbsp;-</td>
                </tr>`

    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_order_management_a').click();
        $('#sidebar_option_order_management_purchase_order').addClass('active');
    };


    /*
    * =========================================================================
    *                      LOGO ATTACHMENT
    * =========================================================================
    **/

    showPreview = () => {
        $(document).on('change', '#logo-button', function(event) {
            if(event.target.files.length > 0){
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
        // hide term note, It will only visible if any term Added
        $('#term_note').parent().parent().hide()
    }


    /*
    * =========================================================================
    *                      CALCULATE PRICE
    * =========================================================================
    **/
    calculatePrice = () => {
        let self = this
        $(document).on('change keyup', '.packing, .quantity, .price', function(e) {
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
            discount = 0,
            vat_percentage = 0,
            vat = 0,
            delivery_cost = 0

        const myPromise = new Promise((resolve, reject) => {
            $.each($('.subtotal'), function(i, v){
                sub_total += parseFloat($(v).val())
                $('#sub_total').html(sub_total.toFixed(2))
                $('#total').html(sub_total.toFixed(2))
                total = sub_total
                if (i == $('.subtotal').length -1) {
                    resolve()
                }
            })
        });

        myPromise
            .then(
                () => {
                    discount_percentage = $('#discount_percentage').val()
                    vat_percentage = parseFloat($('#vat_percentage').val())
                    delivery_cost = parseFloat($('#delivery_cost').val())
                    discount = (discount_percentage * sub_total)/100
                    vat = (vat_percentage * (sub_total - discount))/100
                    total = (sub_total + delivery_cost + vat) - discount
                    $('#discount').html(discount.toFixed(2))
                    $('#vat').html(vat.toFixed(2))
                    $('#total').html(total.toFixed(2))
                },
                () => {}
            )
        

        $(document).on('change keyup', '#discount_percentage', function(e) {
            discount_percentage = $(this).val()
            discount = (discount_percentage * sub_total)/100
            vat = (vat_percentage * (sub_total - discount))/100
            total = (sub_total + delivery_cost + vat) - discount
            $('#discount').html(discount.toFixed(2))
            $('#total').html(total.toFixed(2))
        })


        $(document).on('change keyup', '#delivery_cost', function(e) {
            delivery_cost = parseFloat($(this).val())
            if (isNaN(delivery_cost)) {
                $(this).val("0.00").change()
            }
            total = (sub_total + delivery_cost + vat) - discount
            $('#total').html(total.toFixed(2))
        })


        $(document).on('change keyup', '#vat_percentage', function(e) {
            vat_percentage = parseFloat($(this).val())
            vat = (vat_percentage * (sub_total - discount))/100
            if (isNaN(vat)) {
                $(this).val("0.00").change()
            }
            total = (sub_total + delivery_cost + vat) - discount
            $('#vat').html(vat.toFixed(2))
            $('#total').html(total.toFixed(2))
        })
    }


    /*
    * =========================================================================
    *                      PRODUCT GET SET
    * =========================================================================
    **/    
    get_product = () => {
        let product_select = (page==='edit' && this.executed==1) ? '.product' : '.product:last';
        this.executed += 1

        $(product_select).select2({
                minimumInputLength: 3,
                ajax: {
                url: '/api/v1/product/search/',
                dataType: 'json',
                processResults: function (data) {
                // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function(i, v) {
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
        $(document).on('change', '.product', function(e) {
            let data = $(this).select2('data')[0].other
            let tr = $(this).parent().parent()

            // set description
            tr.find('textarea').val(data.description).change()
            // set quantity
            tr.find('.quantity').val(1)
            // set price
            tr.find('.price').val(parseFloat(data.item_price).toFixed(2)).trigger('change')
            tr.find('.price').attr('data-uuid', data.uuid)
            self.calculateTotal()
        })
    }

    get_price_list = () => {
        let self = this
        let selectd_product_price = null;
        $(document).on('dblclick', '.price', function(e) {
            selectd_product_price = $(this)
            let url = "/api/v1/product/" + selectd_product_price.attr('data-uuid') + '/'
            $.ajax({
                url: url,
                type: "GET",
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify('Success', 'success', 3000);
                    let data = resp;
                    Swal.fire({
                        title: 'Price List',
                        html: `
                        <table style="width: 100%;text-align: left;">
                            <tr>
                                <th>Type</th>
                                <th>Price</th>
                                <th>Action</th>
                            </tr>
                            <tr>
                                <td>Minimum Selling Price</td>
                                <td>${parseFloat(data.item_price).toFixed(2)}</td>
                                <td><i class="fa fa-check-square select_price" aria-hidden="true"></i><td>
                            </tr>
                            <tr>
                                <td>Average Price</td>
                                <td>${parseFloat(data.average_cost).toFixed(2)}</td>
                                <td><i class="fa fa-check-square select_price" aria-hidden="true"></i><td>
                            </tr>
                            <tr>
                                <td>Jobber Price</td>
                                <td>${parseFloat(data.jobbar_price).toFixed(2)}</td>
                                <td><i class="fa fa-check-square select_price" aria-hidden="true"></i><td>
                            </tr>
                            <tr>
                                <td>MAP Price</td>
                                <td>${parseFloat(data.map_price).toFixed(2)}</td>
                                <td><i class="fa fa-check-square select_price" aria-hidden="true"></i><td>
                            </tr>
                            <tr>
                                <td>Retail Price</td>
                                <td>${parseFloat(data.retail_price).toFixed(2)}</td>
                                <td><i class="fa fa-check-square select_price" aria-hidden="true"></i><td>
                            </tr>
                            <tr>
                                <td>Single Price</td>
                                <td>${parseFloat(data.single_price).toFixed(2)}</td>
                                <td><i class="fa fa-check-square select_price" aria-hidden="true"></i><td>
                            </tr>
                            <tr>
                                <td>Dealer Price</td>
                                <td>${parseFloat(data.your_price).toFixed(2)}</td>
                                <td><i class="fa fa-check-square select_price" aria-hidden="true"></i><td>
                            </tr>
                        </table>
                        `,
                        icon: 'info'
                    })
                },
                error: function (response) {
                    if (response.status === 422) {
                        $.map(response.responseJSON.details, function (v, i) {
                            $.each(v, function (j, k) {
                                notify(k, 'error', 2000);
                            })
                        });
                    }
                    notify(response.responseText, 'error', 2000);
                }
            });
        })

        $(document).on('click', '.select_price', function(e) {
            let td = $(this).parent().parent().find('td:nth-child(2)')
            let select_price_td = $(this).parent().parent().find('td:nth-child(3)')
            if (!$.isNumeric(td.text())) {
                notify("Need numbers only.", 'error', 2000)
                select_price_td.text('')
                return
            }
            selectd_product_price.val(td.text()).trigger('change')
            notify("Success.", 'success', 2000)
        })
    }


    /*
    * =========================================================================
    *                      ADD ROW
    * =========================================================================
    **/
    add_new_row = () => {
        let self = this

        $('.add_new_item').on('click', function(e){
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

        $(document).on('click', '.remove_row', function(e){
            $(this).closest("tr").remove();
            self.calculateTotal()
        });
    }


    /*
    * =========================================================================
    *                      SET TERM NOTE 
    * =========================================================================
    **/
    show_term_note = () => {
        let self = this

        $(document).on('change', '#terms', function(e){
            if ($('#terms').val() === "") {
                $("#term_note").parent().parent().hide();
            } else {
                $("#term_note").parent().parent().show();
            }            
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
                    $.each(data.data, function(i, v) {
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
        $(document).on('change', '#supplier', function(e) {
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
        let self = this
        $('.save_po').on('click', function (e) {
            // add url
            let url = po_api_url,
                type = "POST"
            // edit url
            if (page==='edit') {
                url = po_api_url + uuid + '/'
                type = "PATCH"
            }
            let data = {};

            data.is_ready_for_processing = $('#is_ready_for_processing').is(":checked")
            data.number = $('#po_number').val()
            data.date = $('#date').val()
            data.due_date = $('#due_date').val()
            data.notes = $('#notes').val()
            data.customer_note = $('#customer_note').val()
            data.data = {}
            data.data.image = $('#logo-preview').attr('src')
            data.data.address = $('#address').val()
            data.data.url = $('#url').val()
            data.data.po_number = $('#po_number').val()
            data.data.order_date = $('#date').val()
            data.data.due_date = $('#due_date').val()
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
            data.data.vat_percentage = $('#vat_percentage').val()
            data.data.vat = $('#vat').text()
            data.data.delivery_cost = $('#delivery_cost').val()
            data.data.total = $('#total').text()
            data.data.terms = $('#terms').val()
            data.data.term_note = $('#term_note').val()
            data.data.products = []

            let _promise = new Promise((resolve, reject) => {
                $('#products').find('tr').each(function (i, el) {
                    if (self.product_already_in_use($(this).find('.product').val()) === true) {
                        notify(`${$(this).find('.product').select2('data')[0].text} already in use. Modification not allowed.`, 
                                'error', 
                            2000
                        );
                        reject()
                    }

                    if(
                        (parseFloat($(this).find('.quantity').val()) < 0) ||
                        (parseFloat($(this).find('.price').val()) < 0)
                    ) {
                        notify(`${$(this).find('.product').select2('data')[0].text} has negative value.`, 
                            'error', 
                            2000
                        );
                        reject()
                            
                    }
                    data.data.products.push({
                        id: $(this).find('.product').val(),
                        product_id: $(this).find('.product').select2('data')[0].text, 
                        uuid: $(this).find('.product').select2('data')[0].other.uuid, 
                        description: $(this).find('.description').val(),
                        packing: $(this).find('.packing').val(),
                        quantity: $(this).find('.quantity').val(),
                        received: "0",
                        pending: $(this).find('.quantity').val(),
                        price: $(this).find('.price').val(),
                        subtotal: $(this).find('.subtotal').val(),
                    })
                });
                resolve()
            })
            
            _promise
                .then(() => {
                    $.ajax({
                        url: url,
                        type: type,
                        data: JSON.stringify(data),
                        dataType: 'json',
                        contentType: "application/json",
                        success: function (resp) {
                            notify('Success', 'success', 3000);
                            if (page==='add') {
                                setTimeout(() => {  window.location.href = po_list_url; }, 4000);
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
                })
                .catch((e) => {
                    notify(`Operation aborted due to invalid transaction. ${e}`, 'error', 3000);
                    console.log('Operation aborted due to invalid transaction.', e)
                })
            
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
                self.edit_data = resp

                $('#is_ready_for_processing').prop('checked', false);
                if(self.edit_data.is_ready_for_processing){
                    $('#is_ready_for_processing').prop('checked', true);
                }
                $('#po_number').val(data.po_number)
                $('#date').val(data.order_date)
                $('#due_date').val(data.due_date)
                $('#logo-preview').attr('src', data.image)
                $('#address').val(data.address)
                $('#url').val(data.url)
                $('#est_receive_date').val(data.est_receive_date)
                $('#requested_shipping').val(data.requested_shipping)
                $('#carrier_shipping').val(data.carrier_shipping)


                // modify the added option manually - add extra data attributes (in addition to id and text)
                $('#supplier').empty().append(
                    `<option value="${data.supplier.id}">${data.supplier.name}</option>`
                )
                
                let $current_option_data = $('#supplier').select2('data').find(function (currentOption) {
                    return currentOption.id == data.supplier.id
                });

                if ($current_option_data) {
                    $current_option_data['other'] = {'company_address': data.supplier.address};
                }


                $('#supplier_address').val(data.supplier.address)
                $('#ship_to').val(data.ship_to)
                $('#bill_to').val(data.bill_to)
                $('#sub_total').text(data.sub_total)
                $('#discount_percentage').val(data.discount_percentage)
                $('#discount').text(data.discount)
                $('#vat_percentage').val(data.vat_percentage || "0")
                $('#vat').val(data.vat || "0")
                $('#delivery_cost').val(data.delivery_cost || "00")
                $('#total').text(data.total)
                $('#customer_note').val(resp.customer_note || data.additional_notes)
                $('#notes').val(resp.notes)
                if (data.terms != "") {
                    $('#terms').val(data.terms).change()
                    $('#term_note').val(data.term_note)
                }
                
                let rows = ''
                $.each(data.products, function (i, v) {
                    rows += `<tr>
                        <td><select class="product" style="width:200px;height:25px">
                        <option value="${v.id}" selected="selected">${v.product_id}</option>
                        </select></td>
                        <td><textarea rows="1" class="description"
                            onkeyup="$(this).css('height', 'auto').css('height', this.scrollHeight + this.offsetHeight - this.clientHeight);"
                            onchange="$(this).css('height', 'auto').css('height', this.scrollHeight + this.offsetHeight - this.clientHeight);"
                        >${v.description}</textarea></td>
                        <td><input class="packing" type="number" value="${v.packing}"></td>
                        <td><input class="quantity" type="number" min="${v.received}" value="${v.quantity}"></td>
                        ${
                            (!self.product_already_in_use(v.id)) ? 
                            `<td><input class="price" type="number" data-uuid=${v.uuid} value="${v.price}"></td>` : 
                            `<td><input class="price" type="number" value="${v.price}"></td>`
                        }
                        <td><input class="subtotal" type="number" value="${v.subtotal}"></td>
                        ${
                            (!self.product_already_in_use(v.id)) ? '<td class="remove_row">&nbsp;&nbsp;&nbsp;&nbsp;-</td>' : '<td></td>'
                        }
                        
                    </tr>`              
                });
                $('#products').empty().append(rows)
                self.get_product()
                $('.description').trigger('change')
                
                $('#products').find('tr').each(function (i, el) {
                    let row = this
                    let product_id = $(row).find('.product').select2('data')[0].id
                    $.each(data.products, function (i, v) {
                        if (v.id == product_id) {
                            $(row).find('.product').html('').select2({
                                data: [{
                                    id: v.id,
                                    text: v.product_id,
                                    other: v
                                }]
                            })
                        }                        
                    })
                });

                // disable modification as already stock updated and PO is locked
                if (resp.is_locked) {
                    self.disable_edit_page_modification()
                }

                self.calculateTotal()
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
    update_stock = () => {
        let self = this
        $('.update_stock').on('click', function (e) {
            Swal.fire({
                title: 'Are you sure?',
                // text: "You won't be able to UPDATE PO anymore!",
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
                        is_locked: !self.edit_data.is_locked,
                    }
                    $.ajax({
                        url: po_api_url + uuid + '/',
                        headers: {"X-CSRFToken": csrf_token},
                        type: "PATCH",
                        data: JSON.stringify(data),
                        dataType: 'json',
                        contentType: "application/json",
                        success: function (resp) {
                            Swal.fire(
                                'UPDATED!',
                                'Stock has been updated for this PO.',
                                'success'
                            );

                            // disable modification as already stock updated and PO is locked
                            self.disable_edit_page_modification()
                            window.location.reload()
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

    /*
    * =========================================================================
    *                       DISABLE EDIT PAGE MODIFICATION
    * =========================================================================
    **/
    disable_edit_page_modification = () => {
        $('.add_new_item, .save_po, .logo-button-label, .fa-paste').hide()
        $('.remove_row').off('click')
        $('input').prop('disabled', true)
        $('textarea').prop('disabled', true)
        $('select').prop('disabled', true)
        $(".update_stock").text('Unlock')
    }

    /*
    * =========================================================================
    *                       CONTROL COPY PASTE
    * =========================================================================
    **/
    control_copy_paste = () => {
        $('#copy_ship_to_into_bill_to').on('click', function(e) {
            $('#bill_to').val($('#ship_to').val())
        })
        $('#copy_bill_to_into_ship_to').on('click', function(e) {
            $('#ship_to').val($('#bill_to').val())
        })
    }

    /*
    * =========================================================================
    *                       FILTER DATATABLE
    * =========================================================================
    **/
    filter_datatable = (table) => {
        $('div.form-group').prepend(`                   
        <div class="custom-control custom-checkbox" style="display: inline-block; padding-left: 0px">
            <input class="form-control form-control-sm  custom-control-input_date_range" name="date_range"> 
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
            // "startDate": moment().startOf('month').format('MM/DD/YYYY'),
            "startDate": '01/01/2020',
            "endDate": moment()
        });
    }

    /*
    * =========================================================================
    *                       CHECK PRODUCT USEAGE
    * =========================================================================
    **/
    product_already_in_use = (id) => {
        let self = this
        let _products = {}
        let _status = false

        if(page === "add") {
            return _status
        }

        // only check if this is po edit 

        $.each(self.edit_data.data.products, function(i, v) {
            _products[`${v['id']}`] = v.received
        })

        if (
            _products.hasOwnProperty(id) && 
            (["", undefined, null, 0, "0"].indexOf(_products[id]) < 0)
        ) {
            _status = true
        }
        return _status
    }

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        if (page==='list') {
            this.list()
        }
        this.select_sidebar_option()
        this.showPreview()
        this.initial_table()
        this.get_product()
        this.set_product()
        this.get_price_list()
        this.get_supplier()
        this.set_supplier()
        this.show_term_note()
        this.add_new_row()
        this.calculatePrice()
        this.remove_existing_row()
        this.print_preview()
        this.control_copy_paste()
        this.save()
        if (page==='edit') {
            this.edit_page_data_set()
            this.update_stock()
        }
        
    }
}


new PurchaseOrder().main();