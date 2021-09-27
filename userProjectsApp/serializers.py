from django.contrib.auth import models
from rest_framework import serializers
from .models import Project, Review

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='profile.user.username')
    class Meta:
        model = Project
        fields = ('project_image', 'title', 'description', 'link','owner',)
        read_only_fields = ('project_image',)
