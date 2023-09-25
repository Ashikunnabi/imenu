import { MenuDocument } from "./menu_document.js";
import { MenuItem } from "./menu_item.js";

/*
* =============================================================================
*                                   PRODUCT
* =============================================================================
**/

class Menu {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_menu_a').click();
        $('#sidebar_option_menu').addClass('active');
    };

    /*
    * =========================================================================
    *                       Menu in Datatable
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
                        title: 'Add menu',
                        id: 'addMenuButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = menu_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete menu',
                        id: 'deleteMenuButton',
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
                                    url: api_urls["menu_list"] + data[0].uuid + '/',
                                    type: "DELETE",
                                    success: function (response) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Menu has been deleted.',
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
                'url': api_urls["menu_list"],
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
                { "title": "Name", "data": "name" },
                { "title": "Type", "data": "type.name" },
                { "title": "End At", "data": "end_at" },
                { "title": "Start At", "data": "start_at" },
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
                    "targets": [5],
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
    *                       MENU TYPE SEARCH
    * =========================================================================
    **/
    type_search = (default_value = null) => {
        $("#type_uuid").select2({
            // dropdownParent: $("#pos_section"),
            allowClear: true,
            placeholder: "Select menu type",
            minimumInputLength: 0,
            ajax: {
                url: api_urls["menu_type_list"],
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
        }
    }

    /*
    * =========================================================================
    *                       Menu add
    * =========================================================================
    **/

    add = () => {
        // add menu
        $(document).on('submit', '#menu_add', function (e) {
            e.preventDefault();
            const menu_add_form = $('#menu_add').parsley();
            let menu_add_form_data = new FormData($('#menu_add')[0]);


            if (menu_add_form.isValid()) {
                // is_active value set
                // if (menu_add_form_data.has('image')) ($("input[name='image']").val() === '') ? menu_add_form_data.delete('image') : '';
                if (menu_add_form_data.has('start_at')) menu_add_form_data.append('start_at', moment($("#start_at")).format());
                if (menu_add_form_data.has('end_at')) menu_add_form_data.append('end_at', moment($("#end_at")).format());
                if (!menu_add_form_data.has('is_active')) menu_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["menu_list"],
                    type: "POST",
                    data: menu_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        // Display a success message
                        notify("Menu has been created successfully.", "success");

                        // Delay the page refresh for 2 seconds (2000 milliseconds)
                        setTimeout(function() {
                            // Refresh the page
                            // location.reload();
                            window.location.href = menu_list_url;
                        }, 2000); // Adjust the delay time as needed
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
    *                       Menu edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        let self = this
        // edit menu form value setup
        $.ajax({
            url: `${api_urls["menu_list"]}${uuid}/`,
            type: "get",
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else if (key === 'start_at') $('[name=' + key + ']', form).val(`${moment(value).format('YYYY-MM-DD')}`);
                        else if (key === 'end_at') $('[name=' + key + ']', form).val(`${moment(value).format('YYYY-MM-DD')}`);
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#menu_edit'), response.data);

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
    *                       Menu edit
    * =========================================================================
    **/

    edit = () => {
        // edit menu
        $(document).on('submit', '#menu_edit', function (e) {
            e.preventDefault();
            const menu_edit_form = $('#menu_edit').parsley();
            let menu_edit_form_data = new FormData($('#menu_edit')[0]);

            if (menu_edit_form.isValid()) {
                if (menu_edit_form_data.has('start_at')) menu_edit_form_data.set('start_at', moment($("#start_at").val()).format("YYYY-MM-DDTHH:mm:ss"));
                if (menu_edit_form_data.has('end_at')) menu_edit_form_data.set('end_at', moment($("#end_at").val()).format("YYYY-MM-DDTHH:mm:ss"));
                if (!menu_edit_form_data.has('is_active')) menu_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: api_urls["menu_list"] + uuid + '/',
                    type: "PATCH",
                    data: menu_edit_form_data,
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
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.select_sidebar_option();
        if (page_type === "list") this.list();
        if (page_type === "add") {
            this.add();
            this.type_search();
        };
        if (page_type === "edit") {
            this.edit_form_value_set();
            this.edit();
        }
    }
}



new Menu().main();
new MenuItem().main();
new MenuDocument().main();
