from django.contrib import admin
#
# from .models import User
#
# admin.site.register(User)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User

class CustomUserChangeForm(UserChangeForm):
    pass


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ('phone_number', 'invite_code', 'invite_code_for_users')
    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'invite_code', 'invite_code_for_users')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )


# Настройте административную панель для вашей модели User
admin.site.register(User, CustomUserAdmin)