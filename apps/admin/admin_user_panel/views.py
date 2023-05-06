from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                                    SALES REPS
===============================================================================
"""


def sales_reps_list(request):
    if "sub_tab_user_management_sales_reps" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_user_panel/sales_reps/list.html')


def sales_reps_add(request):
    if "sub_tab_user_management_sales_reps" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_user_panel/sales_reps/add.html')


def sales_reps_edit(request, uuid):
    if "sub_tab_user_management_sales_reps" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_user_panel/sales_reps/edit.html', context)
