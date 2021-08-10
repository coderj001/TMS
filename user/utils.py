from rest_framework.permissions import BasePermission


class IsAdminOrTaxAccountant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and (
                request.user.user_type == 'admin' or request.user.user_type == 'tax-accountant'
            )
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.user_type == 'admin'
        )


class IsTaxAccountant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.user_type == 'tax-accountant'
        )


class IsTaxPayer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.user_type == 'tax-payer'
        )
