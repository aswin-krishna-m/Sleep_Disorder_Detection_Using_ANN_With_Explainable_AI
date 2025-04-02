# Generated by Django 5.1.4 on 2025-03-03 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=150)),
                ('lname', models.CharField(max_length=150)),
                ('dob', models.DateField(default='2001-01-01')),
                ('gender', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('password', models.CharField(max_length=150)),
                ('created_on', models.DateField(default='2025-01-01')),
            ],
        ),
    ]
