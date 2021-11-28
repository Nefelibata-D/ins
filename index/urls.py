from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]