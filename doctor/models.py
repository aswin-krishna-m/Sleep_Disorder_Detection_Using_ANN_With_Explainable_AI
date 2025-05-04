from django.db import models
from users.models import Doctor,Patient
from siteAdmin.logger import create_log
from users.models import Doctor

class DoctorQualification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=255)
    year_of_completion = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.degree} ({self.doctor.fname})"

class DoctorExperience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='experiences')
    hospital = models.CharField(max_length=255)
    position = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)  # null if still working

    def __str__(self):
        return f"{self.position} at {self.hospital} ({self.doctor.fname})"

class Consulting(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    started_on = models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.pk is None:
            action = "Consulting"
            details = f"{self.patient.fname} {self.patient.lname} started consulting {self.doctor.fname} {self.doctor.lname} since {self.started_on}."
            create_log(self.patient, action, details)  
        super(Consulting, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.patient.fname} {self.patient.lname} - {self.doctor.fname} {self.doctor.lname}"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,blank=True,null=True)
    message = models.CharField(max_length=255,null=True,blank=True,default=None)
    date = models.DateField()
    time = models.TimeField()
    status_choices = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=20, choices=status_choices, default="Pending")
    created_on = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.pk is None:
            action = "Appointment"
            details = f"New appointment for {self.patient.fname} {self.patient.lname} with {self.doctor.fname} {self.doctor.lname} on {self.date} at {self.time}."
            create_log(self.patient, action, details)
        if self.status == "Confirmed":
            consulting, created = Consulting.objects.get_or_create(doctor=self.doctor, patient=self.patient)
            
        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Appointment - {self.patient.fname} {self.patient.lname} with {self.doctor.fname} {self.doctor.lname} on {self.date} at {self.time}"
    
    
class Diagnosis(models.Model):
    consulting = models.ForeignKey(Consulting, on_delete=models.CASCADE, related_name="diagnoses")
    diagnosis_date = models.DateField(auto_now_add=True)
    sleep_disorder = models.CharField(max_length=255)  
    confidence_score = models.FloatField(null=True, blank=True)  
    notes = models.TextField(null=True, blank=True) 
    def save(self, *args, **kwargs):
        if self.pk is None:  
            action = "Diagnosis"
            details = f"Diagnosis recorded: {self.sleep_disorder} for {self.consulting.patient.fname} {self.consulting.patient.lname}."
            create_log(self.consulting.doctor, action, details)
        super(Diagnosis, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.consulting.patient.fname} {self.consulting.patient.lname} - {self.sleep_disorder} ({self.diagnosis_date})"

class Prescription(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name="prescriptions")
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)  
    duration = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return f"{self.medication_name} for {self.diagnosis.sleep_disorder} - {self.prescribed_on}"

class Prediction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='predictions')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='predictions')
    date = models.DateField(auto_now_add=True)
    predicted_disease = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if self.pk is None:  
            action = "Prediction"
            details = f"Prediction was made: {self.predicted_disease} for {self.patient.fname} {self.patient.lname}."
            create_log(self.doctor, action, details)
        super(Prediction, self).save(*args, **kwargs)
    def __str__(self):
        return f"Prediction for {self.patient} by {self.doctor if self.doctor else 'System'} on {self.date}"