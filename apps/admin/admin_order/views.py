from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                                    ORDER
===============================================================================
"""


def order_list(request):
    if "sub_tab_order_management_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_order/order/list.html')


def order_edit(request, uuid):
    if "sub_tab_order_management_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_order/order/edit.html', context)


"""
===============================================================================
                                FINALE INVOICE
===============================================================================
"""


def finale_invoice_list(request):
    if "sub_tab_order_management_finale_invoice" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_order/finale_invoice/list.html')


def finale_invoice_edit(request, uuid):
    if "sub_tab_order_management_finale_invoice" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_order/finale_invoice/edit.html', context)



"""
===============================================================================
                                SALES ORDER 
===============================================================================
"""


def sales_order_list(request):
    if "sub_tab_order_management_sales_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_order/sales_order/list.html')


def sales_order_add(request):
    if "sub_tab_order_management_sales_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_order/sales_order/add.html')


def sales_order_edit(request, uuid):
    if "sub_tab_order_management_sales_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_order/sales_order/edit.html', context)



"""
===============================================================================
                                PURCHASE ORDER 
===============================================================================
"""


def purchase_order_list(request):
    if "sub_tab_order_management_purchase_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_order/purchase_order/list.html')


def purchase_order_add(request):
    if "sub_tab_order_management_purchase_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_order/purchase_order/add.html')


def purchase_order_edit(request, uuid):
    if "sub_tab_order_management_purchase_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_order/purchase_order/edit.html', context)



"""
===============================================================================
                            MANUFACTURER INVOICE
===============================================================================
"""


def manufacturer_invoice_list(request):
    if "sub_tab_order_management_manufacturer_invoice" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_order/manufacturer_invoice/edit.html')
    