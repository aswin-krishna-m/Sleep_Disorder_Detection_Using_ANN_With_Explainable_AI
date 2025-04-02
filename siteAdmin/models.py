from django.db import models

class Log(models.Model):
    ACTION_CHOICES = (
        ("Patient Registered", "Patient Registered"),
        ("Doctor Registered", "Doctor Registered"),
        ("Appointment Created", "Appointment Created"),
        ("Appointment Updated", "Appointment Updated"),
        ("Diagnosis Made", "Diagnosis Made"),
        ("Prediction Made", "Prediction Made"),
    )
    
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    user_type = models.CharField(max_length=255, blank=True, null=True) 
    user_id = models.CharField(max_length=255, blank=True, null=True) 
    details = models.TextField() 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.user_type} -  {self.user_id} at {self.timestamp}"