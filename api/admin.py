from django.contrib import admin
from .models import *


@admin.register(ShortPath)
class ShortPathAdmin(admin.ModelAdmin):
    list_display = ['id', 'shortcode', 'name', 'download_url', 'file_path', 'time']
