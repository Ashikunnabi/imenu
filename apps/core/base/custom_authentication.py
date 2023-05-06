from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header


class CustomBasicAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        try:
            email = request.META.get('HTTP_X_EMAIL')
        except AttributeError:
            email = None

        try:
            password = request.META.get('HTTP_X_PASSWORD')
        except AttributeError:
            password = None

        if not email or not password:
            user = getattr(request._request, 'user', None)
            if user and not user.is_anonymous:
                return user, None

            auth = get_authorization_header(request).split()

            if not auth or auth[0].lower() != b'basic':
                # raise exceptions.AuthenticationFailed(
                #     'You are logout due to session timeout. Please login.')
                return None

        # check user credentials are valid or not
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                user = user
        except get_user_model().DoesNotExist:
            user = None

        if not user:
            # email/password doesn't matched with any registered user
            return None

        if not user.is_active or int(user.status) != 1:
            raise exceptions.AuthenticationFailed(
                'Your account is inactive. Please contact with administrator. '
                'Thank you')

        if timezone.now() > user.expiry_date:
            raise exceptions.AuthenticationFailed(
                'Your account has been expired. Please contact with '
                'administrator. Thank you')

        return user, None

    def authenticate_header(self, request):
        pass
