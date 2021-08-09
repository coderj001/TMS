from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from tax.models import Tax
from tax.serializers import TaxSerializers, TaxHistorySerializers, TaxReqSerializers
from user.models import User
from user.utils import (
    IsAdmin,
    IsAdminOrTaxAccountant,
    IsTaxAccountant
)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q


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
        return Response(serializer.data)
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
                tax.income = int(data.get('income'))
                tax.deadline = set_date(data.get('deadline'))
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


@swagger_auto_schema(method='get', manual_parameters=[created_at, updated_at])
@api_view(['GET'])
@permission_classes([IsAuthenticated, AllowAny])
def list_tax(request, *args, **kwargs):
    """
    Get list of tax according to hierarchy of users. From point 2.
    """
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
        tax = tax.filter(status=status)
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
    return Response(serializer.data)
