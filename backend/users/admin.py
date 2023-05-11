from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Friends, Notification, User

admin.site.unregister(Group)


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_user', 'second_user')
    search_fields = ('id', 'first_user', 'second_user')
    list_filter = ('first_user', 'second_user')
    empty_value_display = '-empty-'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_from', 'user_to')
    search_fields = ('id', 'user_from', 'user_to')
    list_filter = ('user_from', 'user_to')
    empty_value_display = '-empty-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    search_fields = ('id', 'username', 'email', 'last_name', 'is_staff', 'is_active')
    list_filter = ('first_name', 'last_name', 'is_staff', 'is_active')
    empty_value_display = '-empty-'
