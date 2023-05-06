from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                            POS
===============================================================================
"""


def product_image_list(request):
    # if "sub_tab_others_product_images" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
    #     return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_pos/pos.html')

