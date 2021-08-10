from django.urls import path

from tax.views import (
    edit_tax,
    list_tax,
    request_tax,
    tax_history,
    tax_payment
)

app_name = "tax"

urlpatterns = [
    path('create/', request_tax, name="create_tax"),
    path('list/', list_tax, name="list_tax"),
    path('edit/<int:id>/', edit_tax, name="edit_tax"),
    path('payment/<int:id>/', tax_payment, name="tax_payment"),
    path('list/<int:id>/history/', tax_history, name="tax_history"),
]
