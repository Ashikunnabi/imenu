from django.urls import path, include


app_name = 'main'


urlpatterns = [
    path('', include('apps.main.inventory.urls')),
    # path('', include('apps.main.finale_inventory.urls')),
    # path('', include('apps.main.user_panel.urls')),
    # path('', include('apps.main.shop.urls')),
]
