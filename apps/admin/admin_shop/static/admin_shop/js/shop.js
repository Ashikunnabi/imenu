/*
* =============================================================================
*                             Shop
* =============================================================================
**/

class Shop {
    executed = 0
    edit_data = {}

    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_shop_management_a').click();
        $('#sidebar_option_shop_management_shop').addClass('active');
    };


    /*
    * =========================================================================
    *                      Shops in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#shopDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B><"extra_btn">flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add SO',
                        id: 'addSOButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = add_view_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete SO',
                        id: 'deleteSOButton',
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
                                    url: so_api_url + data[0].uuid + '/',
                                    headers: { "X-CSRFToken": csrf_token },
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'SO has been deleted.',
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
                'url': list_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    notify(error, 'error', 3000);
                    console.log(x, status, error)
                },
            },
            "rowCallback": function (row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Name", "data": "name" },
                { "title": "Location", "data": "location" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                // {
                //     "targets": [2],
                //     "visible": true,
                //     "searchable": true,
                //     "render": function (data, type, row, meta) {
                //         return `${moment(data).format('YYYY-MM-DD')}`;
                //     },
                // },
            ],
        });

        // Single click row select the row and mark a different color
        $('#shopDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#shopDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };


    /*
    * =========================================================================
    *                      SAVE SHOP
    * =========================================================================
    **/
    save = () => {
        let self = this
        $(document).on("click", '.save, .save_info', function (e) {
            // add url
            let url = list_api_url,
                type = "POST"
            // edit url
            if (page === 'edit') {
                url = list_api_url + uuid + '/'
                type = "PATCH"
            }

            let data = {};
            data.name = $('#name').val();
            data.location = $('#location').val();
            data.phone_numbers = $('#phone_numbers').val();
            data.is_active = $('#is_active').is(":checked");
            $.ajax({
                url: url,
                type: type,
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify('Success', 'success', 3000);
                    if (page === 'add') {
                        setTimeout(() => { window.location.href = list_view_url; }, 4000);
                    }
                },
                error: function (response) {
                    notify(response.responseText, 'error', 3000);
                    console.log(response)
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
            url: list_api_url + uuid + '/',
            type: "GET",
            success: function (resp) {
                let data = resp.data
                self.edit_data = data

                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }
                populate($('#shop_info_edit'), data);
            },
            error: function (response) {
                notify(response.responseText, 'error', 3000);
                console.log(response)
            }
        });
    }

    /*
   * =========================================================================
   *                       Employee
   * =========================================================================
   **/
    employees = () => {
        let self = this;
        $.ajax({
            url: list_user_api_url,
            type: "get",
            success: function (response) {
                let html = "";
                $.each(response.data, function (i, v) {
                    html += `
                        <option value=${v.id}>${v.name} (${v.email})</option>
                    `
                })
                $('#employee_list').append(html)
                $('#employee_list').multiSelect({
                    selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='Search for select'>",
                    selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='Search selected'>",
                    afterInit: function (ms) {
                        var that = this,
                            $selectableSearch = that.$selectableUl.prev(),
                            $selectionSearch = that.$selectionUl.prev(),
                            selectableSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selectable:not(.ms-selected)',
                            selectionSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selection.ms-selected';

                        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
                            .on('keydown', function (e) {
                                if (e.which === 40) {
                                    that.$selectableUl.focus();
                                    return false;
                                }
                            });

                        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
                            .on('keydown', function (e) {
                                if (e.which == 40) {
                                    that.$selectionUl.focus();
                                    return false;
                                }
                            });
                    },
                    afterSelect: function () {
                        this.qs1.cache();
                        this.qs2.cache();
                    },
                    afterDeselect: function () {
                        this.qs1.cache();
                        this.qs2.cache();
                    }
                });
            },
            complete: function (data) {
                $.ajax({
                    url: list_shopekeeper_api_url,
                    type: "get",
                    success: function (response) {
                        let employee = $.map(response.data, function (val, i) { return (val.employee) })
                        $('#employee_list').multiSelect('select', employee.map(String))
                        self.save_employee()
                    },
                    error: function (response) {
                        $('#nav-employees').hide()
                        notify('Something went wrong in employees tab', 'error', 5000);
                        console.log(response)
                    }
                });
            },
            error: function (response) {
                $('#nav-employees').hide()
                notify('Something went wrong in employees tab', 'error', 5000);
                console.log(response)
            }
        });

    }


    /*
    * =========================================================================
    *                       SAVE EMPLOYEE DATA 
    * =========================================================================
    **/
    save_employee = () => {
        let self = this
        $(document).on("click", '.save_employee', function (e) {
            let data = {};
            data.employee = $('#employee_list').val();
            $.ajax({
                url: list_shopekeeper_api_url,
                type: "POST",
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify("Success", 'success', 3000);
                },
                error: function (response) {
                    notify(response.responseText, 'error', 3000);
                    console.log(response)
                }
            });
        });
    }


    /*
    * =========================================================================
    *                      Shop Product in Datatable
    * =========================================================================
    **/
    shop_product = () => {
        let self = this;

        let table = $('#shopProductDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            // "dom": '<"mb-3"B><"extra_btn">flrtip',
            "dom": 'flrtip',

            "lengthMenu": [30, 50, 75, 100, 200],
            "ajax": {
                'url': list_shop_product_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    notify(error, 'error', 3000);
                    console.log(x, status, error)
                },
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Product ID", "data": "product_id" },
                { "title": "Stock", "data": "stock" },
                { "title": "Status", "data": "is_active" },
                { "title": "Save", "data": "" },
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
                    "render": function (data, type, row, meta) {
                        let text_color = row.is_shop_product ? "#555" : "#FF0000"
                        let html = `<input type="text" class="shop_product_uuid" id="shop_product_uuid_${row.uuid}" value="${row.uuid}" hidden>
                        <span style="color:${text_color}">${data} <a href="/admin/product/edit/${row.uuid}/" target="_blank"> <i class="fa fa-link" aria-hidden="true"></i></a></span>`
                        return html;
                    },
                },
                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let html = `<input type="number" class="shop_product_stock" id="shop_product_stock_${row.uuid}" value="${data}" min="0">`
                        return html;
                    },
                },
                {
                    "targets": [3],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let html = `<input type="checkbox" class="shop_product_checkbox" id="shop_product_checkbox_${row.uuid}">`
                        if (row.is_active) {
                            html = `<input type="checkbox" class="shop_product_checkbox" id="shop_product_checkbox_${row.uuid}" checked>`
                        }
                        return html;
                    },
                },
                {
                    "targets": [4],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let html = `<i class="fas fa-save shop_product_save" style="color: #4e73df" id="shop_product_save_${row.uuid}"></i>`
                        return html;
                    },
                },
            ],
        });

        // Single click row select the row and mark a different color
        // $('#shopProductDataTable tbody').on('click', 'tr', function () {       
        //     let checkbox = $(this).find(".shop_product_checkbox")     
        //     if (!checkbox.is(":checked")) {
        //         checkbox.prop("checked", true);
        //     } else {
        //         checkbox.prop("checked", false);
        //     }
        // });
        self.save_shop_product()
    };


    /*
    * =========================================================================
    *                       SAVE SHOP PRODUCT DATA 
    * =========================================================================
    **/
    save_shop_product = () => {
        let self = this
        $(document).on("click", '.shop_product_save', function (e) {
            let data = {};
            let product_uuid = $(this).attr("id").replace("shop_product_save_", "")
            data.product_uuid = $('#shop_product_uuid_' + product_uuid).val();
            data.stock = $('#shop_product_stock_' + product_uuid).val();
            data.is_active = $('#shop_product_checkbox_' + product_uuid).is(":checked");
            $.ajax({
                url: list_shop_product_api_url,
                type: "POST",
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                success: function (resp) {
                    notify("Success", 'success', 3000);
                },
                error: function (response) {
                    notify(response.responseText, 'error', 3000);
                    console.log(response)
                }
            });
        });
    }


    /*
    * =========================================================================
    *                      Shop Order in Datatable
    * =========================================================================
    **/
    shop_order = () => {
        let self = this;

        let table = $('#shopOrderDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            // "dom": '<"mb-3"B><"extra_btn">flrtip',
            "dom": 'flrtip',

            "lengthMenu": [30, 50, 75, 100, 200],
            "ajax": {
                'url': list_shop_order_api_url,
                'type': 'GET',
                'error': function (x, status, error) {
                    notify(error, 'error', 3000);
                    console.log(x, status, error)
                },
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Date", "data": "updated_at" },
                { "title": "Order No", "data": "" },
                { "title": "Total", "data": "total" },
                { "title": "Status", "data": "status" },
                { "title": "View", "data": "" },
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
                    "render": function (data, type, row, meta) {
                        return `${moment(data).format('YYYY-MM-DD')}`
                    },
                },
                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let html = `H0000${row.id}`
                        return html;
                    },
                },
                {
                    "targets": [4],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return data;
                    },
                },
                {
                    "targets": [5],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let html = `<i class="fa fa-eye order_details" aria-hidden="true" data-uuid=${row.uuid} data-toggle="modal" data-target="#exampleModalCenter"></i>`
                        return html;
                    },
                },
            ],
        });
    };


    /*
    * =========================================================================
    *                      Shop Order Details Modal
    * =========================================================================
    **/
    shop_order_details = () => {
        let self = this;
        $(document).on('click', '.order_details', function (e) {
            let uuid = $(this).attr("data-uuid")
            $.ajax({
                url: "/api/v1/shop-order/" + uuid + "/",
                type: "GET",
                success: function (resp) {
                    self.shop_order_details_modal(resp)
                },
                error: function (response) {
                    notify(response.responseText, 'error', 5000);
                }
            });
        })
    };

    data
    shop_order_details_modal(data) {
        let html = `
            <tr>
                <td>Sub Total</td>
                <td></td>
                <td>${data.sub_total}</td>
                <th></th>
            </tr>
            <tr>
                <td>Discount</td>
                <td></td>
                <td>${data.discount}</td>
                <th></th>
            </tr>
            <tr>
                <td>Tax</td>
                <td></td>
                <td>${data.tax}</td>
                <th></th>
            </tr>
            <tr>
                <td>Total</td>
                <td></td>
                <td>${data.total}</td>
                <th></th>
            </tr>
        `
        $("#order_details_modal_body .table1 tbody").html("")
        $("#order_details_modal_body .table1 tfoot").html("")
        $.map(data.order_lines, function (product, i) {
            $("#order_details_modal_body .table1 tbody").append(`
                <tr>
                    <td class="product-name">${product.product_id}</td>
                    <td class="product-quantity">${product.quantity}</td>
                    <td>${product.price}</td>
                </tr>
            `)
        })
        $("#order_id").html(data.id)
        $("#order_details_modal_body .table1 tfoot").append(html)
        return html
    }

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        this.select_sidebar_option()
        // call this function to execute all operations of this class
        if (page === 'list') {
            this.list()
        }
        this.save()
        if (page === 'edit') {
            this.edit_page_data_set()
            this.employees()
            this.shop_product()
            this.shop_order()
            this.shop_order_details()
        }
    }
}


new Shop().main();