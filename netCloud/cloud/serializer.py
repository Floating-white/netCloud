from rest_framework import serializers

from .models import User, SubRecord


class UserSerial(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'is_subscribe', 'disk_remaining', 'disk_total']


class SubRecordSerial(serializers.ModelSerializer):
    class Meta:
        model = SubRecord
        fields = ['subscribe_at', 'subscribe_type']