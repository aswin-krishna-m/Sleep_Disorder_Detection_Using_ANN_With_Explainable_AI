from django.shortcuts import render,redirect,get_object_or_404 
from users.models import Doctor,Patient 
from doctor.models import Consulting,Appointment,Prescription,Diagnosis,Prediction
from users.decorators import doctor_login_required
from django.contrib import messages
from .ml_model.predict import predict_sleep_disorder
import math

@doctor_login_required()
def doctorHome(request):
    doctor = get_object_or_404(Doctor,id=request.session['doctor_id'])
    return render(request,'doctor/doctor-home.html',{'doctor': doctor})

@doctor_login_required()
def doctorPatientList(request):
    doctor = get_object_or_404(Doctor,id=request.session['doctor_id'])
    consultations = Consulting.objects.filter(doctor=doctor)
    return render(request, 'doctor/patient-list.html', {'consultations': consultations,})

@doctor_login_required()
def doctorPatientInfo(request,id):
    doctor = get_object_or_404(Doctor,id=request.session['doctor_id'])
    patient = get_object_or_404(Patient,id=id)
    consultation = get_object_or_404(Consulting,doctor=doctor,patient=patient)
    return render(request, 'doctor/patient-view.html', {'consultation': consultation})

@doctor_login_required()
def doctorAppointments(request):
    status_filter = request.GET.get('status', 'All')
    doctor = get_object_or_404(Doctor,id=request.session['doctor_id'])
    
    # Count the number of appointments per status
    all_count = Appointment.objects.filter(doctor=doctor).count()
    pending_count = Appointment.objects.filter(doctor=doctor,status="Pending").count()
    confirmed_count = Appointment.objects.filter(doctor=doctor,status="Confirmed").count()
    completed_count = Appointment.objects.filter(doctor=doctor,status="Completed").count()
    cancelled_count = Appointment.objects.filter(doctor=doctor,status="Cancelled").count()

    # Apply the status filter
    if status_filter != "All":
        appointments = Appointment.objects.filter(doctor=doctor,status=status_filter).select_related("patient").order_by('date')
    else:
        appointments = Appointment.objects.filter(doctor=doctor).order_by('date')
    context = {
        "appointments": appointments,
        "status_filter": status_filter,
        "all_count": all_count,
        "pending_count": pending_count,
        "confirmed_count": confirmed_count,
        "completed_count": completed_count,
        "cancelled_count": cancelled_count,
    }
    return render(request, "doctor/appointment-list.html", context)


@doctor_login_required()
def doctorAppointmentInfo(request,id):
    appointment =  get_object_or_404(Appointment,id=id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Appointment.status_choices):
            appointment.status = new_status
            appointment.save()
        return redirect("doctorAppointmentInfo", id=id)
    return render(request, 'doctor/appointment-view.html', {'appointment': appointment})

@doctor_login_required()
def doctorAddPatient(request):
    doctor = get_object_or_404(Doctor, id=request.session['doctor_id'])
    
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")

        if not dob:
            messages.error(request, "DOB not valid")
            return redirect("doctorAddPatient")

        patient, created = Patient.objects.get_or_create(
            email=email,
            defaults={
                "fname": fname,
                "lname": lname,
                "phone": phone,
                "gender": gender,
                "dob": dob,
                "password": password
            }
        )

        if created:
            messages.success(request, "Patient created successfully.")
        else:
            messages.warning(request, "Patient already exists.")

        # Add patient to consulting
        Consulting.objects.get_or_create(doctor=doctor, patient=patient)
        
        return redirect("doctorPatientList")

    return render(request, "doctor/add-patient.html")


@doctor_login_required()
def doctorProfile(request):
    doctor = Doctor.objects.get(id=request.session['doctor_id'])
    return render(request, 'doctor/profile.html', {'doctor': doctor})

@doctor_login_required()
def doctorProfileEdit(request):
    doctor = get_object_or_404(Doctor, id=request.session['doctor_id'])
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
        return redirect("doctorProfile")
    return render(request, 'doctor/doctor-edit.html', {'doctor': doctor})

@doctor_login_required()
def diagnose(request,id):
    patient = Patient.objects.get(id=id)
    doctor = get_object_or_404(Doctor, id=request.session['doctor_id'])
    if request.method == "POST":
        input_data = {
            "Gender": patient.gender,
            "Age": patient.age,
            "Occupation": request.POST.get("occupation"),
            "Sleep Duration": float(request.POST.get("sleep_duration")),
            "Quality of Sleep": int(request.POST.get("quality_of_sleep")),
            "Physical Activity Level": int(request.POST.get("physical_activity")),
            "Stress Level": int(request.POST.get("stress_level")),
            "BMI Category": request.POST.get("bmi_category"),
            "Systolic": int(request.POST.get("systolic")),
            "Diastolic": int(request.POST.get("diastolic")),
            "Heart Rate": int(request.POST.get("heart_rate")),
            "Daily Steps": int(request.POST.get("daily_steps")),
        }       
        prediction = predict_sleep_disorder(input_data)
        if isinstance(prediction["PredictedDisorder"], float) and math.isnan(prediction["PredictedDisorder"]):
            prediction["PredictedDisorder"] = "Normal"
        Prediction.objects.create(doctor=doctor,patient=patient,predicted_disease=prediction['PredictedDisorder'])   

        return render(request, 'doctor/diagnose.html',{'pid':patient.id,'prediction':prediction,})
    return render(request, 'doctor/diagnose.html')

@doctor_login_required()
def saveDiagnosis(request,id):
    patient = Patient.objects.get(id=id)
    doctor = get_object_or_404(Doctor,id=request.session['doctor_id'])
    if request.method == "POST":
        consulting = Consulting.objects.get(patient=patient,doctor=doctor)
        sleep_disorder = request.POST.get("prediction")
        confidence_score = float(request.POST.get("confidence_score"))
        notes = request.POST.get("notes")
        # Save diagnosis
        diagnosis = Diagnosis.objects.create(
            consulting=consulting,
            sleep_disorder=sleep_disorder,
            confidence_score=confidence_score,
            notes=notes
        )
        # Save prescriptions
        medications = request.POST.getlist("medication_name[]")
        dosages = request.POST.getlist("dosage[]")
        frequencies = request.POST.getlist("frequency[]")
        durations = request.POST.getlist("duration[]")

        for i in range(len(medications)):
            Prescription.objects.create(
                diagnosis=diagnosis,
                medication_name=medications[i],
                dosage=dosages[i],
                frequency=frequencies[i],
                duration=durations[i] if durations[i] else None
            )
        return redirect("doctorHome")  # Redirect to a diagnosis list page
    return redirect("doctorHome")
@doctor_login_required()
def diagnosisHistory(request, id):
    patient = Patient.objects.get(id=id)
    doctor = get_object_or_404(Doctor,id=request.session['doctor_id']) 
    diagnoses = Diagnosis.objects.filter(consulting__doctor=doctor, consulting__patient=patient).order_by('-diagnosis_date')
    context = {
        'patient': patient,
        'diagnoses': diagnoses
    }
    return render(request, 'doctor/diagnose-list.html', context)

@doctor_login_required()
def diagnosisDetail(request,did):
    diagnosis = get_object_or_404(Diagnosis, id=did)
    patient = diagnosis.consulting.patient
    return render(request,'doctor/diagnosis-details.html',{'patient':patient,'diagnosis':diagnosis})


@doctor_login_required()
def doctorReports(request):
    doctor = Doctor.objects.get(id=request.session['doctor_id'])  # Assuming `Doctor` is linked to `User`
    # Count statistics
    total_patients = Consulting.objects.filter(doctor=doctor).count()
    total_appointments = Appointment.objects.filter(doctor=doctor, status="Completed").count()
    total_diagnoses = Diagnosis.objects.filter(consulting__doctor=doctor).count()
    # Fetch latest diagnoses
    diagnoses = Diagnosis.objects.filter(consulting__doctor=doctor).select_related('consulting').order_by('-diagnosis_date')

    context = {
        "doctor": doctor,
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "total_diagnoses": total_diagnoses,
        "diagnoses": diagnoses,
    }
    
    return render(request, "doctor/doctor-reports.html", context)


