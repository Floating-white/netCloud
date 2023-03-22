from rest_framework import serializers

from .models import User, SubRecord, File


class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_subscribe', 'disk_remaining', 'disk_total']


class SubRecordSerial(serializers.ModelSerializer):
    class Meta:
        model = SubRecord
        fields = ['subscribe_at', 'subscribe_type']


class FileSerial(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'file_type', 'file_size']
