from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Client, Session, Package, \
        AttendanceLog
from .serializers import ClientSerializer, SessionSerializer, \
        PackageSerializer, AttendanceLogSerializer
from django.db.models import Q
from pytz import timezone


# Vista para gestionar clientes
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=["post"], url_path="assign_package")
    def assign_package(self, request, pk=None):
        client = self.get_object()
        package_id = request.data.get("package_id")

        if not package_id:
            return Response({"error": "Debe proporcionar un paquete."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            return Response({"error": "Paquete no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar las clases del cliente
        client.available_slots += package.slot_count
        client.save()

        # Crear un registro en AttendanceLog
        AttendanceLog.objects.create(
            client=client,
            action="add",
            slots=package.slot_count,
            description=package.name,
        )

        return Response({"message": "Paquete asignado correctamente."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="attendance_logs")
    def attendance_logs(self, request, pk=None):
        client = self.get_object()
        logs = client.attendance_logs.all()  # Obtiene todos los AttendanceLogs del cliente
        serialized_logs = [
            {
                "action": log.action,
                "slots": log.slots,
                "description": log.description,
                "date": log.date.strftime("%d-%m-%Y %I:%M %p"),  # Formato de fecha amigable
            }
            for log in logs
        ]
        return Response(serialized_logs)


# Vista para gestionar sesiones
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=True, methods=["post"], url_path="mark_attendance")
    def mark_attendance(self, request, pk=None):
        session = self.get_object()

        # Verificar si la sesión ya está terminada
        if session.status == "finished":
            return Response({"error": "La sesión ya está terminada."}, status=status.HTTP_400_BAD_REQUEST)

        client_ids = request.data.get("attended_clients", [])

        # Asegúrate de que los clientes proporcionados estén asignados a esta sesión
        session_clients = session.clients.all()
        assigned_client_ids = [client.id for client in session_clients]

        # Filtrar los clientes que realmente están asignados a esta sesión
        valid_clients = Client.objects.filter(Q(id__in=client_ids) & Q(id__in=assigned_client_ids))

        # Convertir la hora de la sesión al huso horario de Lima, Perú
        lima_tz = timezone("America/Lima")
        session_datetime_lima = session.date.astimezone(lima_tz)
        formatted_date = session_datetime_lima.strftime("%d-%m-%Y %I:%M %p")

        # Mapear tipos de sesión a sus nombres en español
        session_type_map = {
            "private": "Privada",
            "group": "Grupal"
        }
        session_type_translated = session_type_map.get(session.session_type, session.session_type)

        # Descontar una clase de cada cliente que asistió
        for client in valid_clients:
            if client.available_slots > 0:
                client.available_slots -= 1
                client.save()

                # Crear un registro de AttendanceLog
                AttendanceLog.objects.create(
                    client=client,
                    action="deduct",
                    slots=-1,  # Disminuir una clase
                    description=f"Sesión {session_type_translated} - {formatted_date} en {session.get_room_display()}",
                )

        # Marcar la sesión como terminada
        session.status = "finished"
        session.save()

        return Response({"message": "Asistencia marcada correctamente."}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # Aquí puedes hacer validaciones o ajustes si es necesario
        return super().create(request, *args, **kwargs)


# Vista para gestionar paquetes
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class AttendanceLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer
