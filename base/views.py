from django.shortcuts import render,redirect
from .models import *
from .forms import PatientForm
# Create your views here.


def home(request):
    return render(request,'base/home.html')

def start(request):
    return render(request, 'base/Start.html')

######################################## patient crud
def add_patient(request):
    if request.method=="POST":
        patient=Patient.objects.create(
            FullName=request.POST.get("fullname"),
            DOB=request.POST.get("dob"),
            Gender=request.POST.get("patient_gender"),
            Address=request.POST.get("address")
        )
        patient.save()
        return redirect('patient')
        # return render(request,'home')
    return render(request,'base/add_patient.html')


def patient(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    patients=Patient.objects.filter(FullName__icontains=q)
    context={'patients':patients}
    return render(request,'base/patient.html',context)

def remove_patient(request,pk):
    patient=Patient.objects.get(PatientID=pk)
    print(patient)
    patient.delete()
    return redirect('patient')

def edit_patient(request,pk):
    patient=Patient.objects.get(PatientID=pk)
    if request.method=="POST":
        patient.FullName=request.POST.get("fullname")
        patient.Gender=request.POST.get("patient_gender")
        patient.DOB=request.POST.get("dob")
        patient.Address=request.POST.get("address")
        patient.save()
        return redirect('patient')
    patient=Patient.objects.get(PatientID=pk)
    context={'patient':patient}
    print(patient.DOB)
    return render(request,'base/edit_patient.html',context)

def add_patient_mobile(request,pk):
    if request.method=="POST":
        patient=Patient.objects.filter(PatientID=pk)
        mobilenumber=Patient_ContactDetails.objects.create(
        PatientID=patient[0],
        ContactDetails=request.POST.get("mobile_number"))
        mobilenumber.save()
        return redirect('patient')
    return render(request,'base/add_mobile.html')


############################### doctor crud
def doctor(request):
    q=request.GET.get("q") if request.GET.get("q")!=None else '' 
    doctors=Doctor.objects.prefetch_related("doctor_contactdetails_set").filter(Name__icontains=q)
    context={'doctors':doctors}
    return render(request,'base/doctors.html',context)

def add_doctor(request):
    if request.method=="POST":
        doctor=Doctor.objects.create(
            Name=request.POST.get('doctor_name'),
            Specialization=request.POST.get("doctor_specialization")
        )
        doctor.save()
        mobilenumber=Doctor_ContactDetails.objects.create(
            DoctorID=doctor,
            ContactDetails=request.POST.get("mobile_number"))
        mobilenumber.save()
        return redirect('doctors')
    specializationList=Doctor.specializationList
    context={'specializations':specializationList}
    return render(request,'base/add_doctor.html',context)

def edit_doctor(request,pk):
    doctor=Doctor.objects.get(DoctorID=pk)
    if request.method=="POST":
        doctor.Name=request.POST.get("name")
        doctor.Specialization=request.POST.get("doctor_specialization")
        doctor.save()
        return redirect('doctors')
    specializationList=Doctor.specializationList
    context={'specializations':specializationList}
    context={'doctor':doctor,'specializations':specializationList}
    return render(request,'base/edit_doctor.html',context)

def remove_doctor(request,pk):
    doctor=Doctor.objects.get(DoctorID=pk)
    print(doctor)
    doctor.delete()
    return redirect('doctors')

def add_doctor_mobile(request,pk):
    if request.method=="POST":
        doctor=Doctor.objects.filter(DoctorID=pk)
        mobilenumber=Doctor_ContactDetails.objects.create(
        DoctorID=doctor[0],
        ContactDetails=request.POST.get("mobile_number"))
        mobilenumber.save()
        return redirect('doctors')
    return render(request,'base/add_mobile.html')

#-----------------------------------------------------------------------------
############################## Appointment
def appointment(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    appointments=Appointment.objects.filter(PatientID__FullName__icontains=q)
    print(appointments)
    context={'appointments':appointments}
    return render(request,'base/Appointment.html',context)

def add_appointment(request):
    if request.method == 'POST':
        patient_name=request.POST.get('patient_id')  
        patient_id=Patient.objects.filter(FullName=patient_name)
        doctor_name = request.POST.get('doctor_name')  
        doctor_id=Doctor.objects.filter(Name=doctor_name)
        print(patient_id)
        print(doctor_id)
        Appointment.objects.create(
            Required_Specialization=doctor_id[0].Specialization,
            PatientID=patient_id[0],
            DoctorID=doctor_id[0],
        )
        return redirect('appointment')
    patients=Patient.objects.all()
    doctors=Doctor.objects.all()
    context={'patients':patients,"doctors":doctors}
    return render(request,'base/add_appointment.html',context)

def remove_appointment(request,pk):
    appointment=Appointment.objects.get(AppointmentID=pk)
    print(doctor)
    appointment.delete()
    return redirect('appointment')



############################## Discharge

def discharge(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    discharges=Discharge.objects.filter(AdmissionID__PatientID__FullName__icontains=q)
    context={'discharges':discharges}
    return render(request, 'base/Discharge.html',context)

def add_discharge(request,pk):
    if  request.method=="POST":
        reason=request.POST.get('reason')
        addmission=Admission.objects.filter(AdmissionID=pk)
        discharge=Discharge.objects.create(
            AdmissionID=addmission[0],
            Reason=reason
        )
        discharge.save()
        return redirect('discharge')
    return render(request,'base/add_discharge.html')

def remove_discharge(request,pk):
    discharge=Discharge.objects.filter(DischargeID=pk)
    discharge.delete()
    return redirect('discharge')

############################## Stay Details and it's dependent view
def staydetails(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    details=StayDetails.objects.prefetch_related("staydetails_meals_set",
    "staydetails_administeredtreatments_set","staydetails_conditionupdates_set").filter(
        AdmissionID__PatientID__FullName__icontains=q)
    context={'staydetails':details}
    return render(request, 'base/Staydetails.html',context)

def add_admin_tratment(request,pk):
    if request.method=="POST":
        details=StayDetails.objects.filter(StayDetailsID=pk)
        word=request.POST.get("admin_treatment")
        admin_treatment=StayDetails_AdministeredTreatments.objects.create(
            StayDetailsID=details[0],
            AdministeredTreatments=word
        )
        admin_treatment.save()
        return  redirect('staydetails')
    return render(request,'base/add_admin_treatment.html')

def add_condition_update(request,pk):
    if request.method=="POST":
        details=StayDetails.objects.filter(StayDetailsID=pk)
        word=request.POST.get("condition_update")
        condition_update=StayDetails_ConditionUpdates.objects.create(
                StayDetailsID=details[0],
                ConditionUpdates=word
            )
        condition_update.save()
        return  redirect('staydetails')
    return render(request,'base/add_condition_update.html')

def add_meal(request,pk):
    if request.method=="POST":
        details=StayDetails.objects.filter(StayDetailsID=pk)
        word=request.POST.get("meal")
        meal=StayDetails_Meals.objects.create(
                StayDetailsID=details[0],
                Meals=word
            )
        meal.save()
        return  redirect('staydetails')
    return render(request,'base/add_meals.html')

def add_staydetails(request,pk):
    admission=Admission.objects.filter(AdmissionID=pk)
    staydetails=StayDetails.objects.create(
        AdmissionID=admission[0]
    )
    staydetails.save()
    return redirect('staydetails')

def remove_staydetails(request,pk):
    details=StayDetails.objects.filter(StayDetailsID=pk)
    details.delete()
    return redirect('staydetails')


#------------------------------Room ---------------------------
## Room Crud
def room(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms = Room.objects.filter(RoomNumber__icontains=q)
    context = {'rooms': rooms}
    return render(request, 'base/Room.html', context)

def add_room(request):
    if request.method == "POST":
        available=request.POST.get('availability')
        if available=="Available":
            available=True
        else:
            available=False
        room = Room.objects.create(
            RoomNumber=request.POST.get('room_number'),
            Type=request.POST.get('room_type'),
            Availability=available
        )
        room.save()
        return redirect('room')
    return render(request, 'base/add_room.html')

def remove_room(request, pk):
    room = Room.objects.get(RoomNumber=pk)
    room.delete()
    return redirect('room')

#------------------------------- Treatment ---------------------------
def treatment(request):
    treatments=Treatment.objects.prefetch_related('treatment_medications_set').all()
    context={'treatments':treatments}
    return render(request, 'base/Treatment.html',context)

def remove_treatment(request,pk):
    treatment=Treatment.objects.filter(TreatmentID=pk)
    treatment.delete()
    return redirect('treatment')
def add_treatment(request,pk):
    if request.method=="POST":
        appointment=Appointment.objects.filter(AppointmentID=pk)
        treatment=Treatment.objects.create(
            ProcedureDescription=request.POST.get('Procedure'),
            AppointmentID=appointment[0]
        )
        treatment.save()
        return redirect('treatment')
    return render(request,'base/add_treatment.html')


# def medication(request,pk):
#     meds=Treatment_Medications.objects.filter(TreatmentID=pk)
#     context={'meds':meds}
#     return render(request,'base/medications.html',context)


def add_medicine(request,pk):
    if request.POST.get("medicine"):
        treatment=Treatment.objects.filter(TreatmentID=pk)
        medicine=Treatment_Medications.objects.create(
            TreatmentID=treatment[0],
            Medications=request.POST.get('medicine')
        )
        medicine.save()
        return redirect('treatment')
    return render(request,'base/add_medicine.html')


############################### Admission

def add_admission(request,pk):
    if request.method=="POST":
        patient=Patient.objects.filter(PatientID=pk)
        room=Room.objects.filter(RoomNumber=request.POST.get('room_number'))
        admission=Admission.objects.create(
            PatientID=patient[0],
            Reason=request.POST.get('reason'),
            RoomNumber=room[0]
        )
        admission.save()
        return redirect('admission')
    return render(request,'base/add_admission.html')

def remove_admission(request,pk):
    admission=Admission.objects.filter(AdmissionID=pk)
    admission.delete()
    return redirect('admission')

def admission(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    admissions=Admission.objects.filter(PatientID__FullName__icontains=q)
    context={'admissions':admissions}
    return render(request,'base/Admission.html',context)