from django.contrib import admin
from django.contrib.auth.models import Group

from user.forms import UserChangeForm, UserCreationForm
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'email',
        'username',
        'user_type',
        'date_joined'
    )
    list_filter = (
        'user_type',
        'date_joined'
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'email',
                    'password'
                )
            }
        ),
        (
            'Personal info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'user_type',
                    'state'
                )
            }
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_admin',
                    'is_active',
                    'is_superuser',
                    'is_staff'
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'user_type',
                    'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('email', 'username', )
    ordering = ('-date_joined', )


admin.site.unregister(Group)
