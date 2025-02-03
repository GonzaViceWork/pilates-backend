from django.contrib import admin
from .models import Client, Session, Package, AttendanceLog


# Personalización de la interfaz del modelo Client
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "cn_dni", "email", "phone", "available_slots")
    search_fields = ("first_name", "last_name", "cn_dni", "email")
    list_filter = ("available_slots",)
    ordering = ("last_name", "first_name")


# Personalización de la interfaz del modelo Session
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("date", "session_type_display", "status_display", "room_display", "get_clients", "get_attended_clients")
    search_fields = ("date", "clients__first_name", "clients__last_name")
    list_filter = ("session_type", "status", "date", "room")
    ordering = ("date",)

    def get_clients(self, obj):
        return ", ".join([f"{client.first_name} {client.last_name}" for client in obj.clients.all()])
    get_clients.short_description = "Clientes asignados"

    def get_attended_clients(self, obj):
        return ", ".join([f"{client.first_name} {client.last_name}" for client in obj.attended_clients.all()])
    get_attended_clients.short_description = "Clientes asistieron"

    def session_type_display(self, obj):
        return obj.get_session_type_display()
    session_type_display.short_description = "Tipo de sesión"

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = "Estado"
    
    def room_display(self, obj):
        return obj.get_room_display()
    room_display.short_description = "Sala" 


# Personalización de la interfaz del modelo Package
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "slot_count", "price")
    search_fields = ("name",)
    ordering = ("slot_count",)


# Personalización de la interfaz del modelo AttendanceLog
@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ("client", "action_display", "slots", "date", "description")
    search_fields = ("client__first_name", "client__last_name", "action", "description")
    list_filter = ("action", "date")
    ordering = ("-date",)

    def action_display(self, obj):
        return dict(AttendanceLog.ACTION_TYPES).get(obj.action, obj.action)
    action_display.short_description = "Acción"
