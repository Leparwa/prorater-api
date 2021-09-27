
from django.db.models.signals import post_save
from django.dispatch import receiver
from userProjectsApp.models import Project
from authenticationApp.models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)


       