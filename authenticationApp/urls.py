from django.conf.urls import url
from django.urls import path
from .views import LoginView, RegistrationAPIView, UserRetrieveOrUpdateAPIView, VerifyEmail, ProfileRetrieveAPIView

urlpatterns =[
    path('user/register', RegistrationAPIView.as_view(), name="register"),
    path('user/login', LoginView.as_view(), name="login"),
    path('user', UserRetrieveOrUpdateAPIView.as_view()),
    path('user/profile', ProfileRetrieveAPIView.as_view()),
    path('user/verify/', VerifyEmail.as_view(), name='verify-email'),
    
    ]