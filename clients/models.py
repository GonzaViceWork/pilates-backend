from django.db import models

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cn_dni = models.CharField(max_length=15, unique=True)  # CE/DNI único para peruanos y extranjeros
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    available_slots = models.PositiveIntegerField(default=0)  # Clases disponibles

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cn_dni})"


class AttendanceLog(models.Model):
    ACTION_TYPES = [
        ("add", "Paquete Asignado"),
        ("deduct", "Clase Asistida"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="attendance_logs")
    action = models.CharField(max_length=10, choices=ACTION_TYPES)  # "Paquete asignado" o "Clase asistida"
    slots = models.IntegerField()  # Positivo o negativo
    date = models.DateTimeField(auto_now_add=True)  # Fecha y hora del cambio
    description = models.TextField(blank=True)  # Nombre del paquete o clase asistida

    def __str__(self):
        return f"{self.client} - {self.action} ({self.slots})"


class Package(models.Model):
    name = models.CharField(max_length=100)
    slot_count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - S/ {self.price}"


class Session(models.Model):
    SESSION_TYPES = [
        ('group', 'Grupal'),
        ('private', 'Privada'),
    ]
    SESSION_STATUSES = [
        ('pending', 'Pendiente'),
        ('finished', 'Terminada'),
    ]
    ROOM_CHOICES = [
        ('room_201', 'Sala 201'),
        ('room_301', 'Sala 301'),
    ]

    clients = models.ManyToManyField(Client, related_name="sessions", blank=True)
    date = models.DateTimeField()
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES, default='group')
    status = models.CharField(max_length=10, choices=SESSION_STATUSES, default='pending')  # Estado de la sesión
    attended_clients = models.ManyToManyField(Client, related_name="attended_sessions", blank=True)
    room = models.CharField(max_length=10, choices=ROOM_CHOICES, default='room_301')  # Nueva columna

    def __str__(self):
        return f"{self.get_session_type_display()} - {self.date.strftime('%Y-%m-%d %H:%M')} - {self.get_status_display()} en {self.get_room_display()}"
