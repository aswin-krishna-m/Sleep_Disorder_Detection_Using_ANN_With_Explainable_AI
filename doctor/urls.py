from django.urls import path
from . import views

urlpatterns = [
    path("doctorHome/",views.doctorHome, name="doctorHome"),
    path('doctorPatientList/',views.doctorPatientList,name="doctorPatientList"),
    path('doctorPatientInfo/<int:id>/',views.doctorPatientInfo,name="doctorPatientInfo"),
    path('doctorAppointments/',views.doctorAppointments,name="doctorAppointments"),
    path('doctorAppointmentInfo/<int:id>/',views.doctorAppointmentInfo,name="doctorAppointmentInfo"),
    path('doctorAddPatient/',views.doctorAddPatient,name="doctorAddPatient"),
    path('doctorProfile/',views.doctorProfile,name="doctorProfile"),
    path('doctorProfileEdit/',views.doctorProfileEdit,name="doctorProfileEdit"),
    path('diagnose/<int:id>',views.diagnose,name="diagnose"),
    path('saveDiagnosis/<int:id>',views.saveDiagnosis,name="saveDiagnosis"),
    path('diagnosisHistory/<int:id>',views.diagnosisHistory,name="diagnosisHistory"),
    path('diagnosisDetail/<int:did>',views.diagnosisDetail,name="diagnosisDetail"),
    path("doctorReports/", views.doctorReports, name="doctorReports"),

]
