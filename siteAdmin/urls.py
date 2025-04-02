from django.urls import path
from . import views

urlpatterns = [
    path("adminHome/",views.adminHome, name="adminHome"),
    
    path('adminDoctorList/',views.adminDoctorList,name="adminDoctorList"),
    path('adminDoctorInfo/<int:id>/',views.adminDoctorInfo,name="adminDoctorInfo"),
    path('adminDoctorReqList/',views.adminDoctorReqList,name="adminDoctorReqList"),
    path('adminDoctorReqInfo/<int:id>/',views.adminDoctorReqInfo,name="adminDoctorReqInfo"),
    path('toggle_stts/<int:id>/',views.toggle_stts,name="toggle_stts"),
    path('adminEditDoctor/<int:id>/',views.adminEditDoctor,name="adminEditDoctor"),
    path("adminReports/", views.adminReports, name="adminReports"),
    path('adminPatientList/',views.adminPatientList,name="adminPatientList"),
    path('adminPatientInfo/<int:id>/',views.adminPatientInfo,name="adminPatientInfo"),
    path('adminEditPatient/<int:id>/',views.adminEditPatient,name="adminEditPatient"),
    path("logList/", views.logList, name="logList"),
    path("analyze/", views.analyze, name="analyze"),
]

