from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                            PRODUCT IMAGE
===============================================================================
"""


def product_image_list(request):
    if "sub_tab_others_product_images" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_others/product/list.html')


"""
===============================================================================
                            EXPENSE TYPE
===============================================================================
"""


def expense_type_list(request):
    if "sub_tab_others_expense_type" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_others/expense_type/list.html')


"""
===============================================================================
                            EXPENSE
===============================================================================
"""


def expense_list(request):
    if "sub_tab_others_expense" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_others/expense/list.html')

def expense_add(request):
    if "sub_tab_others_expense" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_others/expense/add.html')

def expense_edit(request, uuid):
    if "sub_tab_others_expense" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_others/expense/edit.html', context=context)
