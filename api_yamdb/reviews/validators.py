from datetime import datetime as dt

from rest_framework import serializers


def year_is_not_future(value):
    if value > dt.now().year:
        raise serializers.ValidationError(
            'Год выпуска произведения не может быть больше текущего года.'
        )
    return value
