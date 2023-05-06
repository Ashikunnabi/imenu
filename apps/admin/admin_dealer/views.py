from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                                    DEALER
===============================================================================
"""


def dealer_list(request):
    if "sub_tab_user_management_dealer" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_dealer/dealer/list.html')


def dealer_edit(request, uuid):
    if "sub_tab_user_management_dealer" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'uuid': uuid
    }
    return render(request, 'admin_dealer/dealer/edit.html', context)
