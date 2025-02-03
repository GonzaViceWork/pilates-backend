from rest_framework import serializers
from .models import Client, Session, Package, AttendanceLog


class AttendanceLogSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")  # Formatear fecha de manera amigable

    class Meta:
        model = AttendanceLog
        fields = ['action', 'slots', 'date', 'description']


class ClientSerializer(serializers.ModelSerializer):
    attendance_logs = AttendanceLogSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'cn_dni', 'email', 'phone', 'available_slots', 'attendance_logs']


class SessionSerializer(serializers.ModelSerializer):
    clients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Client.objects.all(),
        required=False
    )
    attended_clients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Client.objects.all(),
        required=False  # Hacer que este campo no sea obligatorio
    )
    session_type_display = serializers.CharField(source="get_session_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    room_display = serializers.CharField(source="get_room_display", read_only=True)

    class Meta:
        model = Session
        fields = [
            'id', 'date', 'room', 'room_display', 'session_type',
            'session_type_display', 'status', 'status_display', 'clients',
            'attended_clients'
        ]


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ["id", "name", "slot_count", "price"]
