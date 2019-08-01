from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
from django.db.models import Model


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return self.serialize_decimal(obj)
        if isinstance(obj, Model):
            return self.serialize_model(obj)
        return super().default(obj)

    def serialize_model(self, instance):
        return instance.pk

    def serialize_decimal(self, raw_decimal):
        return str(raw_decimal)
