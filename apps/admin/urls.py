from django.urls import path, include


app_name = 'admin'


urlpatterns = [
    path('', include('apps.admin.admin_base.urls')),
    path('', include('apps.admin.admin_rbac.urls')),
    path('', include('apps.admin.admin_inventory.urls')),
    path('', include('apps.admin.admin_dealer.urls')),
    path('', include('apps.admin.admin_order.urls')),
    path('', include('apps.admin.admin_others.urls')),
    path('stock-managemnet/', include('apps.admin.admin_stock_management.urls')),
    path('', include('apps.admin.admin_user_panel.urls')),
    path('', include('apps.admin.admin_pos.urls')),
    path('', include('apps.admin.admin_por.urls')),
    path('shop-management/', include('apps.admin.admin_shop.urls')),
    path('', include('apps.admin.admin_menu.urls')),
    path('', include('apps.admin.admin_table.urls')),
]
