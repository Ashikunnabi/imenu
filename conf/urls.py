from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("admin/", include("apps.admin.urls")),
    path("", include("apps.urls")),
]

# static and media url controll
if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True
    )

handler400 = "apps.base.views.handler400"
handler403 = "apps.base.views.handler403"
handler404 = "apps.base.views.handler404"
handler500 = "apps.base.views.handler500"
