import { ProductCode } from "./product_code.js";
import { ProductWarehouse } from "./product_warehouse.js";
import { ProductDocument } from "./product_document.js";
import { ProductPrice } from "./product_price.js";
import { ProductAttribute } from "./product_attribute.js";
import { ProductUnit } from "./product_unit.js";
import { ProductVat } from "./product_vat.js";

/*
* =============================================================================
*                                   PRODUCT
* =============================================================================
**/

class Product {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_inventory_a').click();
        $('#sidebar_option_inventory_product').addClass('active');
    };

    /*
    * =========================================================================
    *                       Product in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#dataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add product',
                        id: 'addProductButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = product_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete product',
                        id: 'deleteProductButton',
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
                                $.ajax({
                                    url: api_urls["product_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Product has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        notify(response.responseText, 'error');
                                    }
                                });
                            }
                        })
                    }
                },
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
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': api_urls["product_list"],
                'type': 'GET',
                'error': function (x, status, error) {
                    console.log(x, status, error)
                },
            },
            "rowCallback": function (row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Code", "data": "code" },
                { "title": "Name", "data": "name" },
                { "title": "Status", "data": "is_active" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                                {
                    "targets": [3],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let active_html = `<i class="fa fa-solid fa-check color_green"></i>`
                        let inactive_html = `<i class="fa fa-times color_red"></i>`
                        if (type === "export") {
                            if (data) return "Active"
                            return "Inactive"
                        }
                        if (data) return active_html
                        return inactive_html
                    },
                },
            ],
        });

        // Single click row select the row and mark a different color
        $('#dataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#dataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       PARENT SEARCH
    * =========================================================================
    **/
    parent_search = (default_value = null) => {
        $("#parent_uuid").select2({
            // dropdownParent: $("#pos_section"),
            allowClear: true,
            placeholder: "Select parent",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["product_list"],
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.uuid,
                            text: `${v.name}`,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });

        if (default_value) {
            let newOption = new Option(default_value.text, default_value.id, true, true);
            $('#parent_uuid').append(newOption).trigger('change');
            console.log(default_value)
        }
    }

    /*
    * =========================================================================
    *                       GROUP SEARCH
    * =========================================================================
    **/
    group_search = (default_value = null) => {
        $("#group_uuid").select2({
            // dropdownParent: $("#pos_section"),
            allowClear: true,
            placeholder: "Select group",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["group_list"],
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.uuid,
                            text: `${v.name}`,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });

        if (default_value) {
            let newOption = new Option(default_value.text, default_value.id, true, true);
            $('#group_uuid').append(newOption).trigger('change');
            console.log(default_value)
        }
    }

    /*
    * =========================================================================
    *                       BRAND SEARCH
    * =========================================================================
    **/
    brand_search = (default_value = null) => {
        $("#brand_uuid").select2({
            // dropdownParent: $("#pos_section"),
            allowClear: true,
            placeholder: "Select brand",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["brand_list"],
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.uuid,
                            text: `${v.name}`,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });

        if (default_value) {
            let newOption = new Option(default_value.text, default_value.id, true, true);
            $('#brand_uuid').append(newOption).trigger('change');
            console.log(default_value)
        }
    }

    /*
    * =========================================================================
    *                       TYPE SEARCH
    * =========================================================================
    **/
    type_search = (default_value = null) => {
        $("#type_uuid").select2({
            // dropdownParent: $("#pos_section"),
            allowClear: true,
            placeholder: "Select type",
            minimumInputLength: 3,
            ajax: {
                url: api_urls["type_list"],
                dataType: 'json',
                processResults: function (data) {
                    // Transforms the top-level key of the response object from 'items' to 'results'
                    let results = []
                    $.each(data.data, function (i, v) {
                        results.push({
                            id: v.uuid,
                            text: `${v.name}`,
                            other: v
                        })
                    })
                    return {
                        results: results
                    };
                }
            }
        });

        if (default_value) {
            let newOption = new Option(default_value.text, default_value.id, true, true);
            $('#type_uuid').append(newOption).trigger('change');
            console.log(default_value)
        }
    }

    /*
    * =========================================================================
    *                       Product add
    * =========================================================================
    **/

    add = () => {
        // add product
        $(document).on('submit', '#product_add', function (e) {
            e.preventDefault();
            const product_add_form = $('#product_add').parsley();
            let product_add_form_data = new FormData($('#product_add')[0]);


            if (product_add_form.isValid()) {
                // is_active value set
                if (product_add_form_data.has('image')) ($("input[name='image']").val() === '') ? product_add_form_data.delete('image') : '';
                if (!product_add_form_data.has('is_active')) product_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["product_list"],
                    type: "POST",
                    data: product_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = product_list_url;
                    },
                    error: function (response) {
                        notify(`${response.responseJSON.message}`, 'error')
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                       Product edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        let self = this
        // edit product form value setup
        $.ajax({
            url: `${api_urls["product_list"]}${uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#product_edit'), response.data);
                self.generate_qr_code(response.data)

                // Select2 parent value set
                if (response.data.parent) {
                    let default_value = {
                        "id": response.data.parent.uuid,
                        "text": response.data.parent.name,
                    }
                    self.parent_search(default_value = default_value);
                } else {
                    self.parent_search();
                }

                // Select2 group value set
                if (response.data.group) {
                    let default_value = {
                        "id": response.data.group.uuid,
                        "text": response.data.group.name,
                    }
                    self.group_search(default_value = default_value);
                } else {
                    self.group_search();
                }

                // Select2 brand value set
                if (response.data.brand) {
                    let default_value = {
                        "id": response.data.brand.uuid,
                        "text": response.data.brand.name,
                    }
                    self.brand_search(default_value = default_value);
                } else {
                    self.brand_search();
                }

                // Select2 type value set
                if (response.data.type) {
                    let default_value = {
                        "id": response.data.type.uuid,
                        "text": response.data.type.name,
                    }
                    self.type_search(default_value = default_value);
                } else {
                    self.type_search();
                }
            },
            error: function (response) {
                notify(`${response.responseJSON.message}`, 'error')
            }
        });
    };

    /*
    * =========================================================================
    *                       Product edit
    * =========================================================================
    **/

    edit = () => {
        // edit product
        $(document).on('submit', '#product_edit', function (e) {
            e.preventDefault();
            const product_edit_form = $('#product_edit').parsley();
            let product_edit_form_data = new FormData($('#product_edit')[0]);

            if (product_edit_form.isValid()) {
                if (!product_edit_form_data.has('is_active')) product_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["product_list"] + uuid + '/',
                    type: "PATCH",
                    data: product_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        notify("Success", 'success')
                    },
                    error: function (response) {
                        notify(`${response.responseJSON.message}`, 'error')
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                       Generate QR code
    * =========================================================================
    **/
    qr_code_html = (path) => {
        $(document).find("#basic_info_qr_code").html("")
        let qr_path = ""
        if (path) {
            qr_path = `
            <a href="${path}" class="d-none d-sm-inline-block btn btn-sm btn-secondary shadow-sm" target="_blank"><i class="fa fa-qrcode"></i></a>
            `
        }
        let html = `
            <label for="code">QR Code:</label><br>
            <a href="#" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm basic_info_generate_qr_code">Generate</a>
            ${qr_path}                            
        `
        $(document).find("#basic_info_qr_code").html(html)
        return html
    }

    generate_qr_code = (data) => {
        let self = this
        self.qr_code_html(data.qr_code_path)

        $(document).on("click", ".basic_info_generate_qr_code", function (e) {
            Swal.fire({
                title: 'Generate QR Code',
                html: `
                    <form id="basic_info_code_qr_code" data-parsley-validate>
                        <div class="row">
                            <div class="col-2">
                                <label for="value" class="font-weight-bold">Value: <span class="text-danger">*</span></label>
                            </div>
                            <div class="col-10">
                                <!--<textarea id="basic_info_code_qr_code_value" cols="30" rows="10">${JSON.stringify(data.code, null, 2)}</textarea>-->
                                <textarea id="basic_info_code_qr_code_value" cols="30" rows="10">${data.code}</textarea>
                            </div>
                        </div>
                    </form>            
                `,
                icon: '',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Save'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: `${api_urls["product_list"]}${data.uuid}/create-qr-code/`,
                        data: JSON.stringify({
                            "data": $("#basic_info_code_qr_code_value").val(),
                        }),
                        type: "POST",
                        contentType: "application/json",
                        success: function (response) {
                            Swal.fire(
                                'Success!',
                                'QR Code has been generated.',
                                'success'
                            );
                            self.qr_code_html(response.data.path)
                        },
                        error: function (response) {
                            $.each(response.responseJSON.error, function (i, v) {
                                notify(`${i.toUpperCase()} - ${v}`, 'error')
                            })
                        }
                    });
                }
            })

        })
    };

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.select_sidebar_option();
        if (page_type === "list") this.list();
        if (page_type === "add") {
            this.add();
            this.parent_search();
            this.group_search();
            this.brand_search();
            this.type_search();
        };
        if (page_type === "edit") {
            this.edit_form_value_set();
            this.edit();
        }
    }
}



new Product().main();
new ProductCode().main();
new ProductWarehouse().main();
new ProductDocument().main();
new ProductPrice().main();
new ProductAttribute().main();
new ProductUnit().main();
new ProductVat().main();
