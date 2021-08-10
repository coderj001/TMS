from django.urls import path

from tax.views import (
    request_tax,
    edit_tax,
    list_tax,
    tax_history
)

app_name = "tax"

urlpatterns = [
    path('create/', request_tax, name="create_tax"),
    path('list/', list_tax, name="list_tax"),
    path('edit/<int:id>/', edit_tax, name="edit_tax"),
    path('list/<int:id>/history/', tax_history, name="tax_history"),
]
