from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from organizations.models import Organization


class UserCountListFilter(admin.SimpleListFilter):
    title = 'ilość pracowników'
    parameter_name = 'users_count'

    def lookups(self, request, model_admin):
        return (
            ('0', '0'),
            ('1-3', '1-3'),
            ('4+', '4+'),
        )

    def queryset(self, request, queryset):

        if self.value() == '0':
            return queryset.filter(
                _users_count=0
            )
        if self.value() == '1-3':
            return queryset.filter(
                _users_count__gt=0,
                _users_count__lt=4
            )
        if self.value() == '4+':
            return queryset.filter(
                _users_count__gte=4
            )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_number',
                    'country', 'url',
                    'users_count')
    list_filter = ('country', UserCountListFilter)
    search_fields = ('tax_number', 'name', 'country')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(_users_count=Count('custom_users'))
        return qs

    def users_count(self, obj):
        if obj._users_count > 3:
            return format_html(
                '<b style="color:{};">{}</b>', 'red', obj._users_count
            )
        return obj._users_count

    users_count.admin_order_field = '_users_count'
    users_count.short_description = 'Ilość pracowników'
