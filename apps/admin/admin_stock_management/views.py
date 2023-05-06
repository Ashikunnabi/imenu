from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                                SALES ORDER 
===============================================================================
"""


def sales_order_list(request):
    if "sub_tab_stock_management_sales_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_stock_management/sales_order/list.html')


def sales_order_add(request):
    if "sub_tab_stock_management_sales_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_stock_management/sales_order/add.html')


def sales_order_edit(request, uuid):
    if "sub_tab_stock_management_sales_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_stock_management/sales_order/edit.html', context)



"""
===============================================================================
                                PURCHASE ORDER 
===============================================================================
"""


def purchase_order_list(request):
    if "sub_tab_stock_management_purchase_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_stock_management/purchase_order/list.html')


def purchase_order_add(request):
    if "sub_tab_stock_management_purchase_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_stock_management/purchase_order/add.html')


def purchase_order_edit(request, uuid):
    if "sub_tab_stock_management_purchase_order" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_stock_management/purchase_order/edit.html', context)




"""
===============================================================================
                                STOCK TRANSACTION 
===============================================================================
"""


def stock_transaction_list(request):
    if "sub_tab_stock_management_stock_transaction" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_stock_management/stock_transaction/list.html')


def stock_transaction_add(request):
    if "sub_tab_stock_management_stock_transaction" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_stock_management/stock_transaction/add.html')


def stock_transaction_edit(request, uuid):
    if "sub_tab_stock_management_stock_transaction" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_stock_management/stock_transaction/edit.html', context)

