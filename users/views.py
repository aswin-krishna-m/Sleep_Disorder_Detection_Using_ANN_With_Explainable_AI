from .models import Admin,Patient,Doctor
from doctor.models import Prediction
from django.shortcuts import render, redirect
from django.contrib import messages
from siteAdmin.logger import create_log

def index(request):
    total_patients = Patient.objects.count()
    total_predictions = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    current_version = "2.0"

    context = {
        "total_patients": total_patients,
        "total_predictions": total_predictions,
        "total_doctors": total_doctors,
        "current_version": current_version,
    }
    return render(request,'index.html',context)

def doctor_register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        specialization = request.POST.get("specialization") 
        license = request.POST.get("license")  
        bio = request.POST.get("bio") 
        if 'profile' in request.FILES:
            profile = request.FILES["profile"]
        else:
            profile = "default/default.jpg"
        
        doctor = Doctor.objects.create(
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            gender=gender,
            password=password,  
            specialization=specialization,
            license=license,
            bio=bio,
            profile_picture = profile
        )
        doctor.save()
        create_log(doctor, "Registration", f"Doctor {doctor.fname} {doctor.lname} registered.")
        messages.success(request, "Registration Success")
        return redirect("login",user_type="Doctor") 
    
    return render(request, "doctor/doctor-reg.html")


def patient_register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        if dob == "":
            messages.error(request, "DOB not valid")
            return redirect("patient_register")
        patient = Patient.objects.create(
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            password=password,  
            gender=gender,
            dob=dob,
        )
        patient.save()
        create_log(patient, "Registration", f"Doctor {patient.fname} {patient.lname} registered.")
        messages.success(request, "Registration Success")
        return redirect("login",user_type="Patient")  

    return render(request, "patient/patient-reg.html")



def user_login(request,user_type):
    if user_type.lower()=="doctor" and 'doctor_id' in request.session:
        return redirect('doctorHome')
    if user_type.lower()=="patient" and 'patient_id' in request.session:
        return redirect('patientHome')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = None
        if user_type.lower()=="doctor":
            try:
                user = Doctor.objects.get(email=email, password=password)
                if not user.stts: 
                    messages.error(request, "Doctor account not yet approved.")
                    return redirect("login",user_type = user_type)
                if user:
                    request.session["doctor_id"] = user.id
                    messages.success(request, "Logged in as Doctor")
                    return redirect("doctorHome")
            except Doctor.DoesNotExist:
                messages.error(request, "User doesn't exist/Invalid credentials")
                return redirect("login",user_type = user_type)

        elif user_type.lower()=="patient":
            try:
                user = Patient.objects.get(email=email, password=password)
                if user:
                    request.session["patient_id"] = user.id
                    messages.success(request, "Logged in as Patient")
                    return redirect("patientHome")
            except Patient.DoesNotExist:
                messages.error(request, "User doesn't exist/Invalid credentials")
                return redirect("login",user_type = user_type)
        return redirect("login",user_type = user_type)
    return render(request, "login.html", {'user_type':user_type})

def admin_login(request):
    if 'admin_id' in request.session:
        return redirect('adminHome')
    if request.method == "POST":
        uname = request.POST.get("uname")
        password = request.POST.get("password")
        user = None
        try:
            user = Admin.objects.get(username=uname, password=password)
            if user:
                request.session["admin_id"] = user.id
                messages.success(request, "Login Success")
                return redirect("adminHome")
        except Admin.DoesNotExist:
            messages.error(request, "User doesn't exist/Invalid credentials")
            return redirect("login")
        return redirect("login")
    return render(request, "adminLogin.html")


def logout(request,user_type):
    if user_type.lower()== "admin":
        del request.session['admin_id']
        messages.success(request, f"{user_type} logged out successfully")
        return redirect('index')
    elif user_type.lower()== "doctor":
        del request.session['doctor_id']
        messages.success(request,  f"{user_type} logged out successfully")
        return redirect('index')
    elif user_type.lower()== "patient":
        del request.session['patient_id']
        messages.success(request,  f"{user_type} logged out successfully")
        return redirect('index')
    else:
        return redirect('index')