from django.urls import include, path
from .views import *


app_name = 'admin_home'

urlpatterns = [
    path('carousel/', include([
        path('', carousel_list, name='carousel_list'),
        path('add/', carousel_add, name='carousel_add'),
        path('edit/<str:hashed_id>/', carousel_edit, name='carousel_edit'),
    ])),
    path('promo-section/', include([
        path('', promo_section_list, name='promo_section_list'),
        path('add/', promo_section_add, name='promo_section_add'),
        path('edit/<str:hashed_id>/', promo_section_edit, name='promo_section_edit'),
    ])),
    path('page/', include([
        path('', page_list, name='page_list'),
        path('add/', page_add, name='page_add'),
        path('edit/<str:hashed_id>/', page_edit, name='page_edit'),
    ])),
    path('banner/', include([
        path('', banner_list, name='banner_list'),
        path('add/', banner_add, name='banner_add'),
        path('edit/<str:hashed_id>/', banner_edit, name='banner_edit'),
    ])),
    path('flyer/', include([
        path('', flyer_list, name='flyer_list'),
        path('add/', flyer_add, name='flyer_add'),
        path('edit/<str:hashed_id>/', flyer_edit, name='flyer_edit'),
    ])),
    path('nav-category/', include([
        path('', nav_category_list, name='nav_category_list'),
        path('add/', nav_category_add, name='nav_category_add'),
        path('edit/<str:hashed_id>/', nav_category_edit, name='nav_category_edit'),
    ])),
    path('notice/', include([
        path('', notice_list, name='notice_list'),
        path('add/', notice_add, name='notice_add'),
        path('edit/<str:hashed_id>/', notice_edit, name='notice_edit'),
    ])),
    path('event/', include([
        path('', event_list, name='event_list'),
        path('add/', event_add, name='event_add'),
        path('edit/<str:hashed_id>/', event_edit, name='event_edit'),
    ])),
    path('useful-link/', include([
        path('', useful_link_list, name='useful_link_list'),
        path('add/', useful_link_add, name='useful_link_add'),
        path('edit/<str:hashed_id>/', useful_link_edit, name='useful_link_edit'),
    ])),
]
