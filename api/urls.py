from django.urls import re_path, path
from . import views

urlpatterns = [
    path('download', views.download, name='download')
]