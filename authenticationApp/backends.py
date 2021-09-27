
import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import CustomUser


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header= authentication.get_authorization_header(request)
        if not auth_header:
            return None
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        token = auth_token[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            id = payload['id']
            user = CustomUser.objects.get(pk=id)
            return (user, token)
        except CustomUser.DoesNotExist as not_found:
            raise exceptions.AuthenticationFailed("user does not exist")
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed("Token is invalid")
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed("Token expired")



        return super().authenticate(request)
