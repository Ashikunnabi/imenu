from django.urls import include, path
from .views import *


app_name = 'home'

urlpatterns = [
    # path('', index, name='index'),
    path(
        'product-details/<str:hashed_id>/',
        product_details,
        name='product_details'
    ),
    path('product-list/', product_list, name='product_list'),
    path('about-us/', about_us, name='about_us'),
    path('available-brands/', brand_list, name='brand_list'),
    path('news-and-updates/', news_and_updates, name='news_and_updates'),
    path('contact-us/', contact_us, name='contact_us'),
    path('advocacy/', advocacy, name='advocacy'),
    path('brand-partner/', brand_partner, name='brand_partner'),
    path('available-brand-pages/', brand_page_list, name='available_brand_pages'),
    path('brand-page/', brand_page, name='brand_page'),
    path('why-buy-from-us/', why_buy_from_us, name='why_buy_from_us'),
    path('shipping-policy/', shipping_policy, name='shipping_policy'),
    path('faq/', faq, name='faq'),
    path('return-policy/', return_policy, name='return_policy'),
    path('marketting/', marketting, name='marketting'),
    path('promotion/', promotion, name='promotion'),
    path('api/', include('apps.home.api.urls'), name='api'),
]
