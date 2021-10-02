from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import permissions

class ProjectListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (permissions.AllowAny,)
    def perform_create(self, serializer):
        serializer.save()
        # serializer.save(owner = self.request.user)
    def get_queryset(self):
        return Project.objects.all()
        # return Project.objects.filter(owner =self.request.user)
class ProjeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field ='id'
    def get_queryset(self):
        return Project.objects.filter(id=self.request.user.profile)
