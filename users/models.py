from django.db import models
from datetime import date

class Admin(models.Model):
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(max_length=254,unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username
    
class Doctor(models.Model):
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    email = models.EmailField( max_length=150,unique=True)
    phone = models.CharField(max_length=15,unique=True,null=True,blank=True)
    gender_choices = (("Male","Male"),("Female","Female"))
    gender = models.CharField(max_length=20,default=None,null=True,blank=True,choices=gender_choices)
    password = models.CharField(max_length=150)
    license = models.CharField(default=None,max_length=255)
    SPECIALIST_CHOICES = (
    ("Neurologist", "Neurologist"),
    ("Psychiatrist", "Psychiatrist"),
    ("Primary Care Physician", "Primary Care Physician"),
    ("Sleep Specialist", "Sleep Specialist"),
    )
    specialization = models.CharField(max_length=50, default=None, null=True, blank=True, choices=SPECIALIST_CHOICES)
    stts = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', default='default/default.jpg', blank=True,null=True)
    bio = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.fname} {self.lname}"
    
class Patient(models.Model):
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    dob = models.DateField(default='2001-01-01')
    gender_choices = (("Male","Male"),("Female","Female"))
    gender = models.CharField(max_length=20,default=None,null=True,blank=True,choices=gender_choices)
    email = models.EmailField( max_length=150,unique=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    password = models.CharField(max_length=150)
    created_on = models.DateField(auto_now_add=True)
    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    def __str__(self):
        return f"{self.fname} {self.lname}"