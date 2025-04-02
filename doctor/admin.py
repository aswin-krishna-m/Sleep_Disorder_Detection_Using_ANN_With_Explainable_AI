from django.contrib import admin
from .models import *

admin.site.register((Consulting,Appointment,Diagnosis,Prescription))