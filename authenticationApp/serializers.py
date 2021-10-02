from django.db.models import query
from django.http import request
from userProjectsApp.serializers import ProjectSerializer
from django.db.models.base import Model
from rest_framework import fields, serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile, CustomUser
from django.contrib import auth


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Profile
        fields = ('username', 'bio', 'photo',)
        read_only_fields = ('username',)
    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('project', {})
    #     for (key, value) in validated_data.items():
    #         setattr(instance, key, value)
    #     for (key, value) in profile_data.items():
    #         setattr(instance.project, key, value)
    #     instance.project.save()
    #     return instance


    


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    project=ProjectSerializer()
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'is_admin',  'profile', 'project',)
        read_only_fields = ('modified',)


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()


        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()
 

        return instance

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128,min_length=2,write_only=True)
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'token',)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
        
# class LoginSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=128, min_length=3, write_only=True)
#     email = serializers.EmailField(max_length=128)
#     username = serializers.CharField(max_length=128, read_only=True)
#     token = serializers.CharField(read_only=True)
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password','token', 'username']
#     def validate(self, attrs):
#         email =attrs.get('email', '')
#         password = attrs.get('password', '')
#         user = auth.authenticate(email=email, password=password)
#         if email is None:
#             raise serializers.ValidationError('An email address is required to log in.')
#         if password is None:
#             raise serializers.ValidationError('A password is required to log in.')
#         if not user:
#             raise AuthenticationFailed('Invalid login credentials')
#         if not user.is_email_verified:
#             raise AuthenticationFailed('Account not activated, please verify your email to activate your account')

#         return {
#             'email': user.email,
#             'username':user.username,
#             'token':user.token
#             }
#         return super().validate(attrs)
        

