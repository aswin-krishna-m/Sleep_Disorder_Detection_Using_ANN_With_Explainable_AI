# Generated by Django 5.1.4 on 2025-03-03 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_doctor_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
