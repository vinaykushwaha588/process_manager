# Generated by Django 5.1.4 on 2024-12-14 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_process_memory_percent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='timestamp',
        ),
    ]