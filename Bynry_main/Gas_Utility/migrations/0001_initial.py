# Generated by Django 5.0.6 on 2024-11-29 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('repair', 'Gas Leak Repair'), ('installation', 'New Installation'), ('maintenance', 'Maintenance')], max_length=20)),
                ('description', models.TextField()),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='uploads/service_requests/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
