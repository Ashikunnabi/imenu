from django.shortcuts import render
from django.http import HttpResponse

from conf.context_processors import current_user_permissions


"""
===============================================================================
                                    CAROUSEL
===============================================================================
"""


def carousel_list(request):
    if "sub_tab_home_page_carousel" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/carousel/list.html')


def carousel_add(request):
    if "sub_tab_home_page_carousel" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/carousel/add.html')


def carousel_edit(request, hashed_id):
    if "sub_tab_home_page_carousel" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/carousel/edit.html', context)


"""
===============================================================================
                                Promo Section
===============================================================================
"""


def promo_section_list(request):
    if "sub_tab_home_page_promo_section" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/promo_section/list.html')


def promo_section_add(request):
    if "sub_tab_home_page_promo_section" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/promo_section/add.html')


def promo_section_edit(request, hashed_id):
    if "sub_tab_home_page_promo_section" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/promo_section/edit.html', context)


"""
===============================================================================
                                Page
===============================================================================
"""


def page_list(request):
    if "sub_tab_home_page_page" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/page/list.html')


def page_add(request):
    if "sub_tab_home_page_page" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/page/add.html')


def page_edit(request, hashed_id):
    if "sub_tab_home_page_page" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/page/edit.html', context)


"""
===============================================================================
                                Banner
===============================================================================
"""


def banner_list(request):
    if "sub_tab_home_page_banner" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/banner/list.html')


def banner_add(request):
    if "sub_tab_home_page_banner" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/banner/add.html')


def banner_edit(request, hashed_id):
    if "sub_tab_home_page_banner" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/banner/edit.html', context)


"""
===============================================================================
                                Flyer
===============================================================================
"""


def flyer_list(request):
    if "sub_tab_home_page_flyer" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/flyer/list.html')


def flyer_add(request):
    if "sub_tab_home_page_flyer" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/flyer/add.html')


def flyer_edit(request, hashed_id):
    if "sub_tab_home_page_flyer" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/flyer/edit.html', context)



"""
===============================================================================
                                NavCategory
===============================================================================
"""


def nav_category_list(request):
    if "sub_tab_home_page_navcategory" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/nav_category/list.html')


def nav_category_add(request):
    if "sub_tab_home_page_navcategory" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/nav_category/add.html')


def nav_category_edit(request, hashed_id):
    if "sub_tab_home_page_navcategory" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/nav_category/edit.html', context)



"""
===============================================================================
                                Notice
===============================================================================
"""


def notice_list(request):
    if "sub_tab_home_page_notice" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/notice/list.html')


def notice_add(request):
    if "sub_tab_home_page_notice" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/notice/add.html')


def notice_edit(request, hashed_id):
    if "sub_tab_home_page_notice" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/notice/edit.html', context)


"""
===============================================================================
                                Event
===============================================================================
"""


def event_list(request):
    if "sub_tab_home_page_event" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/event/list.html')


def event_add(request):
    if "sub_tab_home_page_event" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/event/add.html')


def event_edit(request, hashed_id):
    if "sub_tab_home_page_event" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/event/edit.html', context)


"""
===============================================================================
                                Useful Link
===============================================================================
"""


def useful_link_list(request):
    if "sub_tab_home_page_useful_link" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/useful_link/list.html')


def useful_link_add(request):
    if "sub_tab_home_page_useful_link" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    return render(request, 'admin_home/useful_link/add.html')


def useful_link_edit(request, hashed_id):
    if "sub_tab_home_page_useful_link" not in current_user_permissions(request)["CURRENT_USER_PERMISSIONS"]:
        return HttpResponse("<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access.")
    context = {
        'hashed_id': hashed_id
    }
    return render(request, 'admin_home/useful_link/edit.html', context)
