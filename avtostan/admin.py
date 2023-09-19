from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django.db import models
from django.contrib.auth.models import Group,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



admin.site.unregister(Group)
admin.site.unregister(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name','password', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)