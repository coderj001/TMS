from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_304_NOT_MODIFIED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserSerializerWithToken
)
from user.utils import IsAdminOrTaxAccountant

UserModel = get_user_model()


def index(request):
    return render(request, 'index.html')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerTaxAccountant(request):
    """
    register agent type user
    """
    data = request.data
    try:
        user = UserModel.objects.create_tax_accountant(
            username=data.get('username'),
            email=data.get('email')
        )
        user.set_password(data.get('password'))
        user.save()
        serializer = UserSerializerWithToken(user)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail': 'User with this email alrady exists.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerTaxPayer(request):
    """
    register customer type user
    """
    data = request.data
    try:
        user = UserModel.objects.create_tax_payer(
            username=data.get('username'),
            email=data.get('email')
        )
        user.set_password(data.get('password'))
        user.save()
        serializer = UserSerializerWithToken(user)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail': 'User with this email alrady exists.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrTaxAccountant])
def get_user_list(request, *args, **kwargs):
    """
    get list of users according to hierarchy of admin and agent. From point 1.
    """
    if request.user.user_type == 'admin':
        taxpayer = UserModel.taxpayermanager.all()
        taxaccountant = UserModel.taxaccountantmanager.all()
        query = taxaccountant.union(taxpayer)
        serializer = UserSerializer(query, many=True)
    if request.user.user_type == 'tax-accountant':
        taxpayer = UserModel.taxpayermanager.all()
        serializer = UserSerializer(taxpayer, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, AllowAny])
def get_user_view(request, id, *args, **kwargs):
    """
    get user detail views also according to hierarchy of user. From point 1.
    """
    user = UserModel.objects.get(pk=id)
    if user != request.user:
        if request.user.user_type == 'admin' and user.user_type == 'admin':
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)
        if request.user.user_type == 'tax-accountant' and (
            user.user_type == 'admin' or user.user_type == 'tax-accountant'
        ):
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)
        if request.user.user_type == 'tax-payer' and (
            user.user_type == 'tax-payer' or user.user_type == 'admin' or user.user_type == 'tax-accountant'
        ):
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrTaxAccountant])
def get_user_edit(request, id, *args, **kwargs):
    """
    get edit of user according to hierarchy of admin and agent. From point 1.
    """
    data = request.data
    user = UserModel.objects.get(pk=id)
    if user != request.user:
        if request.user.user_type == 'admin' and user.user_type == 'admin':
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)
        if request.user.user_type == 'tax-accountant' and (
            user.user_type == 'admin' or user.user_type == 'tax-accountant'
        ):
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)
    try:
        serializer.update(instance=user, validated_data=data)
    except Exception as e:
        return Response(
            {'message': 'Invalid Entry.'},
            status=HTTP_304_NOT_MODIFIED
        )
    return Response(serializer.data, status=HTTP_200_OK)
