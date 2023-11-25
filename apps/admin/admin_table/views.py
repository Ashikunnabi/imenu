from django.contrib.auth.decorators import permission_required
from django.shortcuts import render



@permission_required("table.view_table", raise_exception=True)
def table_list(request):
    return render(request, "admin_table/table/list.html")


@permission_required("table.view_table", raise_exception=True)
def table_add(request):
    return render(request, "admin_table/table/add.html")


@permission_required("table.view_table", raise_exception=True)
def table_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_table/table/edit.html", context)

@permission_required("table.view_tabletype", raise_exception=True)
def table_type_list(request):
    return render(request, "admin_table/table_type/list.html")


@permission_required("table.view_tabletype", raise_exception=True)
def table_type_add(request):
    return render(request, "admin_table/table_type/add.html")


@permission_required("table.view_tabletype", raise_exception=True)
def table_type_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_table/table_type/edit.html", context)