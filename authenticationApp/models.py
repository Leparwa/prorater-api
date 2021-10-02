from django.contrib.auth.models import PermissionsMixin, User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models import query
from django.db.models.signals import post_delete, post_save
from django.http import request
import jwt
from datetime import datetime, timedelta
from userProjectsApp.models import Project

def profile_upload(instance, filename):
    return 'user_profile_image/{}/{}'.format(instance.user_id, filename)
def project_upload(instance, filename):
    return 'project_image/{}/{}'.format(instance.user_id, filename)

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('User must have a username.')

        if email is None:
            raise TypeError('User must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
  

class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    email = models.EmailField(unique=True, db_index=True)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_email_verified = models.BooleanField(default=False)
    @property
    def token(self):
        return self._generate_jwt_token()
    EMAIL_FIELD ='email'
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'username':self.username,
            'is_admin':self.is_admin,
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=profile_upload)
    bio = models.CharField(max_length=100)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)


def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
post_delete.connect(delete_user, sender=Profile)