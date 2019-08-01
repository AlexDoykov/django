from json import JSONEncoder
from decimal import Decimal
from .models import Currency


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return self.serializeDecimal(obj)
        if isinstance(obj, Currency):
            return self.serializeCurrency(obj)
        return super().default(obj)

    def serializeCurrency(self, rawCurrency):
        return (rawCurrency.id, )

    def serializeDecimal(self, rawDecimal):
        return str(rawDecimal)
