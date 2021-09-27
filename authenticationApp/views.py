from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers, status, views
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer, ProfileSerializer
from rest_framework import generics 
from .models import CustomUser, Profile
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import HandleUtils
from django.urls import reverse
from userProjectsApp.models import Project
import jwt

class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user_request = request.data
        serializer = self.serializer_class(data=user_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token
        reverse_link = reverse('verify-email')
        absolute_url = 'http://'+get_current_site(request).domain+reverse_link+'?token='+str(token)
        email_body = "Hello"+" " + user.username  +" "+ "click the link bellow to activate your account \n"+absolute_url
        data ={'email_body':email_body, 'email_to':user.email,'email_subject': 'Activate Prorater Account'}
        HandleUtils.sendEmail(data)
        return Response(user_data, status=status.HTTP_200_OK)

class VerifyEmail(views.APIView):
    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, 'HS256',)
            print(payload)
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
            return Response({'message': 'Email Successfully Verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Your Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Token Is Invalid'}, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'data':serializer.validated_data, 'status': status.HTTP_202_ACCEPTED},)

class UserRetrieveOrUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        user_data = request.data
        serializer_data = {
            'username':user_data.get('username', request.user.username),
            'profile':user_data.get('profile'),
            }
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
     
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileRetrieveAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=self.request.user)
            serializer = self.serializer_class(profile)        
        except Profile.DoesNotExist as identifier:
            raise (status.HTTP_302_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
        profile_data = request.user
        serializer_data =request.data
        # queryset =
        serializer_data ={
            'username':profile_data.get('username'),
            'bio':profile_data.get('bio'),
            'photo':profile_data.get('photo'),
            'project':profile_data.get('project', self.request.user)
            }
        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



