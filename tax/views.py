from datetime import datetime

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_204_NO_CONTENT
)

from tax.models import Tax
from tax.serializers import (
    TaxHistorySerializers,
    TaxPaymentSerializers,
    TaxSerializers
)
from user.models import User
from user.utils import (
    IsAdmin,
    IsAdminOrTaxAccountant,
    IsTaxAccountant,
    IsTaxPayer
)


# yyyy/mm/dd
def set_date(sdate):
    var = list(map(int, sdate.split('/')))
    return datetime(var[0], var[1], var[2])


@swagger_auto_schema(method='post', request_body=TaxSerializers)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTaxAccountant])
def request_tax(request, *args, **kwargs):
    """
    Create tax by only tax-accountant type user. From point 2.
    """
    tax_accountant = request.user
    data = request.data
    try:
        tax_payer = User.taxpayermanager.filter(
            Q(username=data.get('tax_payer')) | Q(email=data.get('tax_payer'))).first()
        tax = Tax.objects.create(
            income=int(data.get('income')),
            deadline=set_date(data.get('deadline')),
            tax_accountant=tax_accountant,
            tax_payer=tax_payer
        )
        tax.save()
        serializer = TaxSerializers(tax)
        return Response(serializer.data, status=HTTP_201_CREATED)
    except Exception as e:
        message = {'detail': 'Invalid Parameters.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=TaxSerializers)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsTaxAccountant])
def edit_tax(request, id, *args, **kwargs):
    """
    Edit tax by only tax_accountant type user. From point 4.
    """
    tax_accountant = request.user
    data = request.data
    try:
        tax = Tax.objects.get(pk=id)
        if tax_accountant == tax.tax_accountant:
            if tax.status != 'PAID':
                tax_payer = User.taxpayermanager.filter(
                    Q(username=data.get('tax_payer')) | Q(email=data.get('tax_payer'))).first()
                if data.get('income'):
                    tax.income = int(data.get('income'))
                if data.get('deadline'):
                    tax.deadline = set_date(data.get('deadline'))
                if tax_payer:
                    tax.tax_payer = tax_payer
                tax.save()
                serializer = TaxSerializers(tax)
                return Response(serializer.data)
            else:
                message = {'detail': 'Can\'t edit.'}
                return Response(message, status=HTTP_400_BAD_REQUEST)
        else:
            message = {'detail': 'You don\'t have right to edit.'}
            return Response(message, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        message = {'detail': 'Invalid Parameters.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


created_at = openapi.Parameter(
    'created_at',
    openapi.IN_QUERY,
    description="created_at",
    type=openapi.FORMAT_DATETIME
)
updated_at = openapi.Parameter(
    'updated_at',
    openapi.IN_QUERY,
    description="updated_at",
    type=openapi.FORMAT_DATETIME
)
status = openapi.Parameter(
    'status',
    openapi.IN_QUERY,
    description="Status",
    type=openapi.FORMAT_SLUG
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[status, created_at, updated_at]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, AllowAny])
def list_tax(request, *args, **kwargs):
    """
    Get list of tax according to hierarchy of users. From point 2.
    """
    try:
        user = request.user
        status = request.query_params.get('status')
        created_at = request.query_params.get('created_at')
        updated_at = request.query_params.get('updated_at')

        if user.user_type == 'admin':
            tax = Tax.objects.all().order_by('updated_at')
        if user.user_type == 'tax-accountant':
            tax = user.user_tax_accountant.all().order_by('updated_at')
        if user.user_type == 'tax-payer':
            tax = user.user_tax_payer.all().order_by('updated_at')

        if status:
            tax = tax.filter(status=status.upper())
        if created_at:
            dt = set_date(created_at)
            tax = tax.filter(
                created_at__year=dt.year,
                created_at__month=dt.month,
                created_at__day=dt.day
            )
        if updated_at:
            dt = set_date(updated_at)
            tax = tax.filter(
                updated_at__year=dt.year,
                updated_at__month=dt.month,
                updated_at__day=dt.day
            )

        serializer = TaxSerializers(tax, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as e:
        message = {'detail': 'Error'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrTaxAccountant])
def tax_history(request, id, *args, **kwargs):
    user = request.user
    tax = Tax.objects.get(pk=id)
    try:
        if user.user_type == 'admin' or user.user_type == 'tax-accountant':
            if user.user_type == 'tax-accountant' and user == tax.tax_accountant:
                tax_hist = TaxHistorySerializers(tax)
                return Response(tax_hist.data, status=HTTP_200_OK)
            elif user.user_type == 'admin':
                tax_hist = TaxHistorySerializers(tax)
                return Response(tax_hist.data, status=HTTP_200_OK)
        else:
            return Response(
                'User of tax-payer type not allowed.',
                status=HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        message = {'detail': 'Tax with id not found.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=TaxPaymentSerializers)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTaxPayer])
def tax_payment(request, id, *args, **kwargs):
    user = request.user
    data = request.data
    try:
        tax = Tax.objects.get(pk=id)
    except Exception as e:
        message = {'detail': 'Tax with id not found.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)
    if tax.tax_payer == user:
        serializers = TaxPaymentSerializers(data)
        if (serializers.data.get('income') == tax.total_amount or tax.total_amount == 0) and tax.status != 'PAID':
            tax.payment()
            message = {
                'message': f'Payment of Rs. {tax.total_amount} is success.'}
            return Response(message, status=HTTP_204_NO_CONTENT)
        else:
            message = {'message': f'Amount to be paid Rs.{tax.total_amount}'}
            return Response(message, status=HTTP_204_NO_CONTENT)
    else:
        message = {'detail': 'Tax with id not for current user.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)
