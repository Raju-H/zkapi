# serializer.py
from rest_framework import serializers
from .models import Device

class AttendanceSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    privilege = serializers.CharField()
    group_id = serializers.CharField()
    in_time = serializers.DateTimeField()
    out_time = serializers.DateTimeField(allow_null=True)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'area', 'username', 'ip_address', 'port', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']