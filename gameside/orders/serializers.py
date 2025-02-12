from typing import Iterable

from django.http import HttpRequest

from shared.serializers import BaseSerializer
from games.serializers import GameSerializer


class OrderSerializer(BaseSerializer):
    def __init__(
        self,
        to_serialize: object | Iterable[object],
        *,
        fields: Iterable[str] = [],
        request: HttpRequest = None,
    ):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance):
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'key': instance.key if instance.status == 3 else None,
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'price': instance.price
        }
