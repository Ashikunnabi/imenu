from django.contrib.auth.decorators import permission_required
from django.shortcuts import render



@permission_required("inventory.view_attributegroup", raise_exception=True)
def attribute_group_list(request):
    return render(request, "admin_inventory/attribute_group/list.html")


@permission_required("inventory.view_attributegroup", raise_exception=True)
def attribute_group_add(request):
    return render(request, "admin_inventory/attribute_group/add.html")


@permission_required("inventory.view_attribute_group", raise_exception=True)
def attribute_group_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/attribute_group/edit.html", context)

@permission_required("inventory.view_attribute", raise_exception=True)
def attribute_list(request):
    return render(request, "admin_inventory/attribute/list.html")


@permission_required("inventory.view_attribute", raise_exception=True)
def attribute_add(request):
    return render(request, "admin_inventory/attribute/add.html")


@permission_required("inventory.view_attribute", raise_exception=True)
def attribute_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/attribute/edit.html", context)


@permission_required("inventory.view_brand", raise_exception=True)
def brand_list(request):
    return render(request, "admin_inventory/brand/list.html")


@permission_required("inventory.view_brand", raise_exception=True)
def brand_add(request):
    return render(request, "admin_inventory/brand/add.html")


@permission_required("inventory.view_brand", raise_exception=True)
def brand_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/brand/edit.html", context)


@permission_required("inventory.view_document", raise_exception=True)
def document_list(request):
    return render(request, "admin_inventory/document/list.html")


@permission_required("inventory.view_document", raise_exception=True)
def document_add(request):
    return render(request, "admin_inventory/document/add.html")


@permission_required("inventory.view_document", raise_exception=True)
def document_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/document/edit.html", context)


@permission_required("inventory.view_group", raise_exception=True)
def group_list(request):
    return render(request, "admin_inventory/group/list.html")


@permission_required("inventory.view_group", raise_exception=True)
def group_add(request):
    return render(request, "admin_inventory/group/add.html")


@permission_required("inventory.view_group", raise_exception=True)
def group_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/group/edit.html", context)


@permission_required("inventory.view_product", raise_exception=True)
def product_list(request):
    return render(request, "admin_inventory/product/list.html")


@permission_required("inventory.add_product", raise_exception=True)
def product_add(request):
    return render(request, "admin_inventory/product/add.html")


@permission_required("inventory.change_product", raise_exception=True)
def product_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/product/edit.html", context)


@permission_required("inventory.view_supplier", raise_exception=True)
def supplier_list(request):
    return render(request, "admin_inventory/supplier/list.html")


@permission_required("inventory.view_supplier", raise_exception=True)
def supplier_add(request):
    return render(request, "admin_inventory/supplier/add.html")


@permission_required("inventory.view_supplier", raise_exception=True)
def supplier_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/supplier/edit.html", context)


@permission_required("inventory.view_type", raise_exception=True)
def type_list(request):
    return render(request, "admin_inventory/type/list.html")


@permission_required("inventory.view_type", raise_exception=True)
def type_add(request):
    return render(request, "admin_inventory/type/add.html")


@permission_required("inventory.view_type", raise_exception=True)
def type_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/type/edit.html", context)


@permission_required("inventory.view_warehouse", raise_exception=True)
def warehouse_list(request):
    return render(request, "admin_inventory/warehouse/list.html")


@permission_required("inventory.view_warehouse", raise_exception=True)
def warehouse_add(request):
    return render(request, "admin_inventory/warehouse/add.html")


@permission_required("inventory.view_warehouse", raise_exception=True)
def warehouse_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/warehouse/edit.html", context)


@permission_required("inventory.view_unit", raise_exception=True)
def unit_list(request):
    return render(request, "admin_inventory/unit/list.html")


@permission_required("inventory.view_unit", raise_exception=True)
def unit_add(request):
    return render(request, "admin_inventory/unit/add.html")


@permission_required("inventory.view_unit", raise_exception=True)
def unit_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/unit/edit.html", context)


@permission_required("inventory.view_vat", raise_exception=True)
def vat_list(request):
    return render(request, "admin_inventory/vat/list.html")


@permission_required("inventory.view_vat", raise_exception=True)
def vat_add(request):
    return render(request, "admin_inventory/vat/add.html")


@permission_required("inventory.view_vat", raise_exception=True)
def vat_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_inventory/vat/edit.html", context)
