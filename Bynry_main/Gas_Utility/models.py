from django.db import models
from django.contrib.auth.models import User  # If using Django's built-in User model

class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('repair', 'Gas Leak Repair'),
        ('installation', 'New Installation'),
        ('maintenance', 'Maintenance'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')  # Connect to User
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    file_upload = models.FileField(upload_to='uploads/service_requests/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_service_type_display()} ({self.get_status_display()})"




from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'status', 'submitted_at', 'resolved_at')
    list_filter = ('status', 'service_type')
    search_fields = ('user__username', 'service_type')
