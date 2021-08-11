from django.contrib import admin

from tax.models import Tax


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = (
        'income',
        'status',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'status',
        'created_at',
        'updated_at'
    )
