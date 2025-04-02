from django.shortcuts import render,redirect ,get_object_or_404
from users.decorators import patient_login_required
from datetime import datetime
from users.models import Doctor,Patient
from doctor.models import Consulting,Appointment, Prescription, Diagnosis
from django.contrib import messages


@patient_login_required()
def patientHome(request):
    ptnt = Patient.objects.get(id = request.session["patient_id"])
    return render(request,'patient/patient-home.html',{'ptnt':ptnt})

@patient_login_required()
def doctorList(request):
    doctors = Doctor.objects.filter(stts=True)
    return render(request, 'patient/doctor-list.html', {'doctors': doctors})

@patient_login_required()
def doctorInfo(request,id):
    doctor = Doctor.objects.get(id=id)
    return render(request, 'patient/doctor-view.html', {'doctor': doctor})


@patient_login_required()
def patientProfile(request):
    patient = Patient.objects.get(id=request.session['patient_id'])
    return render(request, 'patient/profile.html', {'patient': patient})

@patient_login_required()
def patientProfileEdit(request):
    patient = get_object_or_404(Patient, id=request.session['patient_id'])
    if request.method == "POST":
        patient.fname = request.POST.get("fname")
        patient.lname = request.POST.get("lname")
        patient.dob = request.POST.get("dob")
        patient.gender = request.POST.get("gender")
        patient.email = request.POST.get("email")
        patient.phone = request.POST.get("phone")
        patient.save()
        messages.success(request, "Patient information updated successfully.")
        return redirect("patientProfile")
    return render(request, 'patient/patient-edit.html', {'patient': patient})

@patient_login_required()
def patientAppointments(request):
    status_filter = request.GET.get('status', 'All')
    patient = get_object_or_404(Patient,id=request.session['patient_id'])
    
    # Count the number of appointments per status
    all_count = Appointment.objects.filter(patient=patient).count()
    pending_count = Appointment.objects.filter(patient=patient,status="Pending").count()
    confirmed_count = Appointment.objects.filter(patient=patient,status="Confirmed").count()
    completed_count = Appointment.objects.filter(patient=patient,status="Completed").count()
    cancelled_count = Appointment.objects.filter(patient=patient,status="Cancelled").count()

    # Apply the status filter
    if status_filter != "All":
        appointments = Appointment.objects.filter(patient=patient,status=status_filter).select_related("doctor").order_by('date')
    else:
        appointments = Appointment.objects.filter(patient=patient).order_by('date')
    context = {
        "appointments": appointments,
        "status_filter": status_filter,
        "all_count": all_count,
        "pending_count": pending_count,
        "confirmed_count": confirmed_count,
        "completed_count": completed_count,
        "cancelled_count": cancelled_count,
    }
    return render(request, 'patient/my-appointments.html',context)

@patient_login_required()
def bookAppointment(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    user = get_object_or_404(Patient, id=request.session['patient_id'])
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if not date or not time or not phone or not message:
            messages.error(request, "All fields are required.")
            return redirect("bookAppointment", id=id)

        try:
            appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
            appointment_time = datetime.strptime(time, "%H:%M").time()

            existing_appointment = Appointment.objects.filter(
                doctor=doctor, patient=user, date=appointment_date, status="Confirmed"
            ).exists()

            if existing_appointment:
                messages.error(request, "You already have a confirmed appointment on this date.")
                return redirect("bookAppointment", id=id)

            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=user,
                date=appointment_date,
                phone=phone,
                time=appointment_time,
                message = message,
            )
            appointment.save()
            messages.success(request, "Appointment request sent successfully! Await confirmation.")
            return redirect("doctorInfo", id=id)

        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect("bookAppointment", id=id)

    return render(request, "patient/appointment.html", {"doctor": doctor})


@patient_login_required()
def consultingList(request):
    patient = get_object_or_404(Patient, id=request.session['patient_id'])
    consulting = Consulting.objects.filter(patient=patient)
    return render(request, 'patient/consult-doctor.html', {'consulting': consulting})

@patient_login_required()
def patientDiagnosisHistory(request,did):
    doctor = get_object_or_404(Doctor, id=did)
    patient = get_object_or_404(Patient, id=request.session['patient_id'])
    consultingList= Consulting.objects.get(doctor=doctor,patient=patient)
    diagnoses = Diagnosis.objects.filter(consulting = consultingList.id).order_by('-diagnosis_date')
    return render(request, "patient/diagnosis-list.html", {"diagnoses": diagnoses,'doc':did})

@patient_login_required()
def patientDiagnosisDetail(request, did):
    diagnosis = get_object_or_404(Diagnosis, id=did)
    return render(request, "patient/diagnosis-details.html", {"diagnosis": diagnosis})
