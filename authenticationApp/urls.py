from django.conf.urls import url
from django.urls import path
from .views import LoginAPIView, RegistrationAPIView, UserRetrieveOrUpdateAPIView, VerifyEmail, ProfileRetrieveAPIView

urlpatterns =[
    path('user/register', RegistrationAPIView.as_view()),
    path('user/login', LoginAPIView.as_view()),
    path('user', UserRetrieveOrUpdateAPIView.as_view()),
    path('user/profile', ProfileRetrieveAPIView.as_view()),
    path('user/verify/', VerifyEmail.as_view(), name='verify-email'),
    
    ]