from django.urls import path
from .views import ProjectListView, ProjeDetailsView
urlpatterns =[
    path('', ProjectListView.as_view()),
    path('<int:id>', ProjeDetailsView.as_view()),
 ]
