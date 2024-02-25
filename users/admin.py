from django.contrib import admin
from .models import *

@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'text', 'date')
