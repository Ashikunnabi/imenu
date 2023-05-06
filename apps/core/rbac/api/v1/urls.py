from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = 'v1'

router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')
# router.register(r'group', GroupViewSet, basename='group')
# router.register(r'permission', PermissionViewSet, basename='permission')
# # router.register(r'user-activity-log', UserActivityLogViewSet, basename='user_activity_log')
# router.register(r'dealer', DealerViewSet, basename='dealer')

urlpatterns = [
    path(
        'users/',
        UserListCreateAPIView.as_view(),
        name='user-list-create'
    ),
    path(
        'users/<uuid:uuid>/',
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name='user-retrieve-update-delete'
    ),
    path(
        'users/staffs/',
        StaffListAPIView.as_view(),
        name='staff-list'
    ),
    path(
        'groups/',
        GroupListCreateAPIView.as_view(),
        name='group-list-create'
    ),
    path(
        'groups/<int:id>/',
        GroupRetrieveUpdateDestroyAPIView.as_view(),
        name='group-retrieve-update-delete'
    ),
    path(
        'permisisons/',
        PermissionListCreateAPIView.as_view(),
        name='permission-list-create'
    ),
    path(
        'permisisons/<int:id>/',
        PermissionRetrieveUpdateDestroyAPIView.as_view(),
        name='permission-retrieve-update-delete'
    ),
    path(
        'update-info',
        update_own_profile_info,
        name='update_own_profile_info'
    ),
    path(
        'last-account-activation-email-sent-at',
        last_account_activation_email_sent_at,
        name='last_account_activation_email_sent_at'
    ),
    path(
        'account-activate',
        active_account_by_activation_url,
        name='active_account_by_activation_url'
    ),
    path('', include(router.urls)),
]
