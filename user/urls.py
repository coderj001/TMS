from django.urls import path

from user.views import (
    MyTokenObtainPairView,
    get_user_edit,
    get_user_list,
    get_user_view,
    registerTaxAccountant,
    registerTaxPayer,
    state_list
)

app_name = "user"

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name="user_login"),
    path('register/tax-accountant/', registerTaxAccountant,
         name="tax_accountant_register"),
    path('register/tax-payer/', registerTaxPayer, name="tax_payer_register"),
    path('list/', get_user_list, name="user_list"),
    path('<uuid:id>/', get_user_view, name="user_view"),
    path('<uuid:id>/edit/', get_user_edit, name="user_edit"),
    path('state_list/', state_list, name="state_list"),
]
