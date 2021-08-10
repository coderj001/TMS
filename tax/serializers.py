from rest_framework.serializers import (
    DictField,
    FloatField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField
)

from tax.models import Tax


class TaxSerializers(ModelSerializer):
    tax_accountant = SerializerMethodField(read_only=True)
    tax_payer = SerializerMethodField()

    class Meta:
        model = Tax
        fields = (
            'id',
            'income',
            'status',
            'tax_amount',
            'tax_accountant',
            'tax_payer',
            'created_at',
            'updated_at',
            'deadline',
            'fines',
            'total_amount',
            'payment_status',
            'payment_date',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'tax_amount': {'read_only': True},
            'fines': {'read_only': True},
            'payment_date': {'read_only': True},
            'payment_status': {'read_only': True},
            'total_amount': {'read_only': True},
        }

    def get_tax_accountant(self, obj):
        return obj.tax_accountant.username

    def get_tax_payer(self, obj):
        return obj.tax_payer.username


class HistoricalRecordField(ListField):
    child = DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())


class TaxHistorySerializers(ModelSerializer):
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Tax
        fields = ('history', )


class TaxPaymentSerializers(Serializer):
    income = FloatField()
