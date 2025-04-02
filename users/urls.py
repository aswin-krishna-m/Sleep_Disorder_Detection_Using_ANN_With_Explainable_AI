from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path("register/doctor/",views.doctor_register, name="doctor_register"),
    path("register/patient/",views.patient_register, name="patient_register"),
    path("adminLogin/",views.admin_login, name="adminLogin"),
    path("login/<str:user_type>/",views.user_login, name="login"),
    path("logout/<str:user_type>/",views.logout,name='logout'),
   
    ]
