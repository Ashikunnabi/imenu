from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                                SHOP 
===============================================================================
"""


def shop_list(request):
    if (
        "shop.view_shop"
        not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]
    ):
        return HttpResponse(
            "<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access."
        )
    return render(request, "admin_shop/shop/list.html")


def shop_add(request):
    if (
        "shop.add_shop"
        not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]
    ):
        return HttpResponse(
            "<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access."
        )
    return render(request, "admin_shop/shop/add.html")


def shop_edit(request, uuid):
    if (
        "shop.view_shop"
        not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]
    ):
        return HttpResponse(
            "<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access."
        )
    context = {"uuid": uuid}
    return render(request, "admin_shop/shop/edit.html", context)


"""
===============================================================================
                            POS
===============================================================================
"""


def shop_pos(request):
    # if "sub_tab_others_product_images" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
    #     return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, "admin_shop/shop/pos.html")
