from django.urls import path
from . import views

urlpatterns = [
    path("patientHome/",views.patientHome, name="patientHome"),
    path('doctorList/',views.doctorList,name="doctorList"),
    path('consultingList/',views.consultingList,name="consultingList"),
    path('doctorInfo/<int:id>/',views.doctorInfo,name="doctorInfo"),
    path('patientAppointments/',views.patientAppointments,name="patientAppointments"),
    path('bookAppointment/<int:id>/',views.bookAppointment,name="bookAppointment"),
    path('patientProfile/',views.patientProfile,name="patientProfile"),
    path('patientProfileEdit/',views.patientProfileEdit,name="patientProfileEdit"),
     path("patientDiagnosisHistory/<int:did>", views.patientDiagnosisHistory, name="patientDiagnosisHistory"),
    path("patientDiagnosisDetail/<int:did>/", views.patientDiagnosisDetail, name="patientDiagnosisDetail"),

]
