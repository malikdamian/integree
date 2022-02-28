from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from account.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

admin.site.site_header = 'Administracja'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_active',
                    'organization', 'date_joined',)
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('email', 'last_name',
                     'organization__name',
                     'organization__tax_number')
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'first_name', 'last_name',
                           'organization', 'alias')}),
        ('Uprawnienia', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1',
                       'password2', 'first_name',
                       'last_name', 'is_staff',
                       'is_active', 'organization')}
         ),
    )

    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
