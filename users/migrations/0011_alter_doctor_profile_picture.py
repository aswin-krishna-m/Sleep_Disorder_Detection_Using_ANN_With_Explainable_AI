# Generated by Django 5.1.4 on 2025-03-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_doctor_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_picture',
            field=models.ImageField(default='default/default.jpg', upload_to='doctor_profiles/'),
        ),
    ]
