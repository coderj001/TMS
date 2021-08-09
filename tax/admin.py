from django.contrib import admin
from simple_history import register
from simple_history.admin import SimpleHistoryAdmin

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
