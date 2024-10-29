# -------- c:/Users/fabri/Repos/_courses/django/api_course/django-recipe-api/app/core/admin.py
""" Admin configuration for the core app """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    """ Define admin page for users """
    ordering = ['id']                                                                   # order the users by id, you can add several fields to order by, e.g. ['id', 'name']

    list_display = ['id', 'name', 'email', 'is_active', 'is_staff', 'is_superuser']     # fields to display in the user list
    search_fields = ('name', 'email')
    list_per_page = 50
    list_display_links = ('id', 'name', 'email')                                         # clickable fields
    add_fieldsets = (                                                                    # fields displayed when adding a new user
        (None, { 'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
                'classes': ('wide',)                                                      # classes to apply to the fieldset, wide makes the fields wider
        }),
    )
    fieldsets = (                                                                         # fields displayed when viewing a user
        (None,{'fields': ('email', 'password')}),                                         # title + fields in the section
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)                  # no need to create a custom admin for the Recipe model, so we just register it with the default admin