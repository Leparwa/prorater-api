
# import jwt

# from django.conf import settings

# from rest_framework import authentication, exceptions

# from .models import CustomUser


# class JWTAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth_header= authentication.get_authorization_header(request)
#         if not auth_header:
#             return None
#         auth_data = auth_header.decode('utf-8')
#         auth_token = auth_data.split(" ")
#         token = auth_token[1]
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
#             id = payload['id']
#             user = CustomUser.objects.get(pk=id)
#             return (user, token)
#         except CustomUser.DoesNotExist as not_found:
#             raise exceptions.AuthenticationFailed("user does not exist")
#         except jwt.DecodeError as identifier:
#             raise exceptions.AuthenticationFailed("Token is invalid")
#         except jwt.ExpiredSignatureError as identifier:
#             raise exceptions.AuthenticationFailed("Token expired")



#         return super().authenticate(request)

from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

def enforce_csrf(request):
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            print(raw_token)
        else:
            raw_token = self.get_raw_token(header)
            print(raw_token)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token