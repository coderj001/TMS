from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'user_type',
            'date_joined'
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }


class UserSerializerWithToken(UserSerializer):
    token = SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'username',
            'user_type',
            'date_joined',
            'token'
        )

        extra_kwargs = {
            'id': {'read_only': True},
            'token': {'read_only': True}
        }

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data
