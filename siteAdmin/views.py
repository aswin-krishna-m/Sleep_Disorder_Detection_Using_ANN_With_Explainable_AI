from django.shortcuts import render,redirect,get_object_or_404
from users.decorators import admin_login_required
from users.models import *
from doctor.models import *
from .models import Log
from django.contrib import messages

# Create your views here.
@admin_login_required()
def adminHome(request):
    return render(request,'siteAdmin/admin-home.html')

@admin_login_required()
def adminDoctorList(request):
    doctors = Doctor.objects.filter(stts=True)
    request_count = Doctor.objects.filter(stts=False).count()
    return render(request, 'siteAdmin/doctor-list.html', {'doctors': doctors,'request_count':request_count})

@admin_login_required()
def adminDoctorInfo(request,id):
    doctor = Doctor.objects.get(id=id)
    return render(request, 'siteAdmin/doctor-view.html', {'doctor': doctor})

@admin_login_required()
def adminDoctorReqList(request):
    doctors = Doctor.objects.filter(stts=False)
    return render(request, 'siteAdmin/doctor-list-req.html', {'doctors': doctors,})

@admin_login_required()
def adminDoctorReqInfo(request,id):
    doctor = Doctor.objects.get(id=id)
    return render(request, 'siteAdmin/doctor-view-req.html', {'doctor': doctor})

@admin_login_required()
def toggle_stts(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.stts = not doctor.stts
    doctor.save()
    messages.success(request, f"Doctor {doctor.fname} {doctor.lname}'s status updated successfully.")
    next_page = request.GET.get('next', 'adminDoctorInfo')
    print(next_page)
    return redirect(next_page, id=id) 

@admin_login_required()
def adminEditDoctor(request,id):
    doctor = get_object_or_404(Doctor, id=id)
    next_page = request.GET.get('next', 'adminDoctorInfo')
    if request.method == "POST":
        doctor.fname = request.POST.get("fname")
        doctor.lname = request.POST.get("lname")
        doctor.email = request.POST.get("email")
        doctor.phone = request.POST.get("phone")
        doctor.gender = request.POST.get("gender")
        doctor.license = request.POST.get("license")
        doctor.specialization = request.POST.get("specialization")
        doctor.bio = request.POST.get("bio")
        if 'profile' in request.FILES:
            doctor.profile_picture = request.FILES["profile"]
        doctor.save()
        messages.success(request, "Doctor information updated successfully.")
        return redirect(next_page, id=id)
    return render(request, 'siteAdmin/doctor-edit.html', {'doctor': doctor})

@admin_login_required()
def adminPatientList(request):
    patients = Patient.objects.all()
    return render(request, 'siteAdmin/patient-list.html', {'patients': patients,})

@admin_login_required()
def adminPatientInfo(request,id):
    patient = Patient.objects.get(id=id)
    return render(request, 'siteAdmin/patient-view.html', {'patient': patient})

@admin_login_required()
def adminEditPatient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        patient.fname = request.POST.get("fname")
        patient.lname = request.POST.get("lname")
        patient.dob = request.POST.get("dob")
        patient.gender = request.POST.get("gender")
        patient.email = request.POST.get("email")
        patient.phone = request.POST.get("phone")
        patient.save()
        messages.success(request, "Patient information updated successfully.")
        return redirect("adminPatientInfo", id=id)

    return render(request, 'siteAdmin/patient-edit.html', {'patient': patient})



@admin_login_required()
def adminReports(request):
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_diagnoses = Diagnosis.objects.count()
    total_predictions = Prediction.objects.count()
    completed_appointments = Appointment.objects.filter(status="Completed").count()
    total_prescriptions = Prescription.objects.count()
    recent_diagnoses = Diagnosis.objects.order_by('-diagnosis_date')[:10]  # Show last 10 diagnoses

    context = {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_diagnoses": total_diagnoses,
        "completed_appointments": completed_appointments,
        "total_prescriptions": total_prescriptions,
        "total_predictions": total_predictions,
        "recent_diagnoses": recent_diagnoses,
    }
    
    return render(request, "siteAdmin/reports.html", context)



@admin_login_required()
def logList(request):
    logs = Log.objects.all().order_by("-timestamp")
    return render(request, "siteAdmin/log-list.html", {"logs": logs})

@admin_login_required()
def analyze(request):
    model_info = {
    'accuracy': '90.11%',
    'f1_score': '90.14%',
    'recall': '90.11%',
    'precision': '90.29%',
    'input_features' : '10',
'hidden_layers': '[64, 32]',
'activation_function': 'relu (hidden), softmax (output)',
'optimizer': 'Adam (learning_rate=0.001)'
    }
    return render(request, "siteAdmin/analyze.html", {"model_info": model_info})
