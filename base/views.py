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
    if request.method == "POST":
        patient = Patient.objects.create(
            Name=request.POST.get("fullname"),
            Date_Of_Birth=request.POST.get("dob"),
            Address=request.POST.get("address"),
            Phone_Number=request.POST.get("phone_number")
        )
        return redirect('patient')
    return render(request, 'base/patient/add_patient.html')


def patient(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    patients = Patient.objects.filter(Name__icontains=q)
    context = {'patients': patients}
    return render(request, 'base/patient/patient.html', context)


def remove_patient(request, pk):
    patient = Patient.objects.get(Patient_ID=pk)
    patient.delete()
    return redirect('patient')


def edit_patient(request, pk):
    patient = Patient.objects.get(Patient_ID=pk)
    if request.method == "POST":
        patient.Name = request.POST.get("fullname")
        patient.Date_Of_Birth = request.POST.get("dob")
        patient.Address = request.POST.get("address")
        patient.Phone_Number = request.POST.get("phone_number")
        patient.save()
        return redirect('patient')
    context = {'patient': patient}
    return render(request, 'base/patient/edit_patient.html', context)


############################### doctor crud
def doctor(request):
    q = request.GET.get("q") if request.GET.get("q") else ''
    doctors = Doctor.objects.filter(Name__icontains=q)
    context = {'doctors': doctors}
    return render(request, 'base/doctor/doctors.html', context)

def add_doctor(request):
    if request.method == "POST":
        doctor = Doctor.objects.create(
            Name=request.POST.get('doctor_name'),
            Specialization=request.POST.get("doctor_specialization"),
            Phone_Number=request.POST.get("Phone_Number"),
            Appointment_Price=request.POST.get("Appointment_Price")
        )
        doctor.save()
        return redirect('doctors')
    specializationList = Doctor.SPECIALIZATION_CHOICES
    context = {'specializations': specializationList}
    return render(request, 'base/doctor/add_doctor.html', context)

def edit_doctor(request, pk):
    doctor = Doctor.objects.get(Doctor_ID=pk)
    if request.method == "POST":
        doctor.Name = request.POST.get("name")
        doctor.Specialization = request.POST.get("doctor_specialization")
        doctor.Phone_Number=request.POST.get("phone_number")
        doctor.Appointment_Price=request.POST.get("Appointment_Price")
        doctor.save()
        return redirect('doctors')
    specializationList = Doctor.SPECIALIZATION_CHOICES
    print(specializationList)
    context = {'doctor': doctor, 'specializations': specializationList}
    return render(request, 'base/doctor/edit_doctor.html', context)

def remove_doctor(request, pk):
    doctor = Doctor.objects.get(Doctor_ID=pk)
    doctor.delete()
    return redirect('doctors')

#-----------------------------------------------------------------------------
############################## Appointment
def appointment(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    appointments=Appointment.objects.filter(Patient_ID__Name__icontains=q)
    print(appointments)
    context={'appointments':appointments}
    return render(request,'base/appointment/Appointment.html',context)

def add_appointment(request):
    if request.method == 'POST':
        patient_name=request.POST.get('patient_id')
        patient_id=Patient.objects.filter(Name__icontains=patient_name)
        doctor_name = request.POST.get('doctor_name')  
        doctor_id=Doctor.objects.filter(Name__icontains=doctor_name)

        appointment=Appointment.objects.create(
            Patient_ID=patient_id[0],
            Doctor_ID=doctor_id[0],
        )
        appointment.save()

        bill=Bill.objects.create(
        Total=doctor_id[0].Appointment_Price,
        Patient_ID=patient_id[0],
        Status='pending',
        Reason=f"Dr {doctor_name} Appointment at {appointment.Date}"
        )
        bill.save()
        return redirect('appointment')
    patients=Patient.objects.all()
    doctors=Doctor.objects.all()
    print(patients)
    print(doctors)
    context={'patients':patients,"doctors":doctors}
    return render(request,'base/appointment/add_appointment.html',context)

def remove_appointment(request,pk):
    appointment=Appointment.objects.get(Appointment_ID=pk)
    print(doctor)
    appointment.delete()
    return redirect('appointment')



############################## Discharge

def discharge(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    discharges=Discharge.objects.filter(Admission_ID__Patient_ID__Name__icontains=q)
    context={'discharges':discharges}
    return render(request, 'base/Discharge.html',context)

from datetime import datetime
from django.shortcuts import get_object_or_404

def add_discharge(request,pk):
    admission=get_object_or_404(Admission,Admission_ID=pk)
    admission.End_Date = datetime.now()
    admission.save()
    End_date_aware = timezone.make_aware(admission.End_Date, timezone=admission.End_Date.tzinfo)
    diff = End_date_aware-admission.Start_Date
    days=diff.days
    roomprice=admission.Room_Number.Room_Price
    patient=admission.Patient_ID
    print(patient)
    bil=Bill.objects.create(
        Total=days*roomprice,
        Status='Pending',
        Patient_ID=patient,
        Reason=f"Admission at {admission.Room_Number} for {days} days"

    )
    bil.save()
    return redirect('admission')


def remove_discharge(request,pk):
    discharge=Discharge.objects.filter(DischargeID=pk)
    discharge.delete()
    return redirect('discharge')

############################## Stay Details and it's dependent view
def add_admin_tratment(request,pk):
    if request.method=="POST":
        admission=Admission.objects.filter(Admission_ID=pk)
        patient=admission[0].Patient_ID
        admintreatment=TreatmentAdmission.objects.create(
            Treatment_Title=request.POST.get("treatment_title"),
            Treatment_Details=request.POST.get("treatment_details"),
            admission=admission[0],
            price=request.POST.get("price")
        )
        bill=Bill.objects.create(
            Total=request.POST.get("price"),
            Patient_ID=patient,
            Status='pending',
        )
        admintreatment.save()
        return redirect('admission')
        
    return render(request,'base/admin_treatment/add_admin_treatment.html')

def admission_treatments(request,pk):
    admission=Admission.objects.filter(Admission_ID=pk)
    admission_treatment=TreatmentAdmission.objects.filter(admission=admission[0])
    context={'admissiontreatment':admission_treatment}
    return render(request,'base/admin_treatment/show_admission_treatments.html',context)

def remove_admission_treatment(request,pk):
    treatment=TreatmentAdmission.objects.filter(Treatment_ID=pk)
    treatment.delete()
    return redirect('admission')

#------------------------------Room ---------------------------
## Room Crud
def room(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms = Room.objects.filter(Room_Number__icontains=q)
    context = {'rooms': rooms}
    return render(request, 'base/room/Room.html', context)

def add_room(request):
    if request.method == "POST":
        room = Room.objects.create(
            Room_Number=request.POST.get('room_number'),
            Room_Type=request.POST.get('room_type'),
            Room_Price=request.POST.get('Room_Price')
        )
        room.save()
        return redirect('room')
    return render(request, 'base/room/add_room.html')

def remove_room(request, pk):
    room = Room.objects.get(Room_Number=pk)
    room.delete()
    return redirect('room')

def edit_room(request,pk):
    room = Room.objects.get(Room_Number=pk)

    if request.method=="POST":
        room.Room_Number=request.POST.get('room_number')
        room.Room_Type=request.POST.get('room_type')
        room.Room_Price=request.POST.get('Room_Price')
        room.save()
        return redirect('room')
    context={"room":room}
    return render(request,'base/room/edit_room.html',context)


#------------------------------- Treatment ---------------------------
def treatment(request):
    treatments=Treatment.objects.all()
    context={'treatments':treatments}
    return render(request, 'base/treatment/Treatment.html',context)

def remove_treatment(request,pk):
    treatment=Treatment.objects.filter(Treatment_ID=pk)
    treatment.delete()
    return redirect('treatment')

def add_treatment(request,pk):
    if request.method=="POST":
        appointment=Appointment.objects.filter(Appointment_ID=pk)
        print(appointment)
        treatment=Treatment.objects.create(
            Procedure=request.POST.get('Procedure'),
            Appointment_ID=appointment[0],
            Disease=request.POST.get("Disease")
        )
        treatment.save()
        return redirect('treatment')
    return render(request,'base/treatment/add_treatment.html')

############################### Admission

def add_admission(request,pk):
    if request.method=="POST":
        patient=Patient.objects.filter(Patient_ID=pk)
        room=Room.objects.filter(Room_Number=request.POST.get('room_number'))
        doctor=Doctor.objects.filter(Name=request.POST.get("doctor_name"))
        admission=Admission.objects.create(
            Patient_ID=patient[0],
            Room_Number=room[0],
            Doctor_ID=doctor[0]
        )
        admission.save()
        return redirect('admission')
    doctors=Doctor.objects.all()
    rooms=Room.objects.all()
    context={'doctors':doctors,'rooms':rooms}
    return render(request,'base/admission/add_admission.html',context)

def remove_admission(request,pk):
    admission=Admission.objects.filter(Admission_ID=pk)
    admission.delete()
    return redirect('admission')

def admission(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    admissions=Admission.objects.filter(Patient_ID__Name__icontains=q)
    context={'admissions':admissions}
    return render(request,'base/admission/Admission.html',context)

def bill(request,pk):
    patient=get_object_or_404(Patient,Patient_ID=pk)
    bills=Bill.objects.filter(Patient_ID=patient,Status="pending")
    print(bills)
    context={'bills':bills}
    return render(request,'base/bill/bill.html' ,context)

def paybill(request,pk):
    bill=get_object_or_404(Bill,Bill_ID=pk)
    bill.Status="Payed"
    bill.save()
    return redirect('patient')

def add_employee(request):
    if request.method=="POST":
        employee=Employee.objects.create(
            Name=request.POST.get("name"),
            Phone_Number=request.POST.get("phone_number"),
            Role=request.POST.get("role")
        )
        employee.save()
        room=get_object_or_404(Room,Room_Number=request.POST.get('room_number'))
        employeeroom=Employee_Room.objects.create(
            Employee_ID=employee,
            Room_Number=room
        )
        return redirect('employee')
    rooms=Room.objects.all()
    context={"rooms":rooms}
    return render(request,'base/employee/add_employee.html',context)

def employee(request):
    employee=Employee.objects.all().prefetch_related('employee_room_set')
    print(employee)
    context={'employees':employee}
    return render(request,'base/employee/employees.html',context)

def remove_employee(request, pk):
    emp = Employee.objects.get(Employee_ID=pk)
    emp.delete()
    return redirect('employee')

def add_employee_room(request,pk):
    if request.method=="POST":
        emp = Employee.objects.get(Employee_ID=pk)
        room = Room.objects.get(Room_Number=request.POST.get('room_number'))

        emproom=Employee_Room.objects.create(
            Employee_ID=emp,
            Room_Number=room
        )
        emproom.save()
        return redirect('employee')
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'base/employee/add_employee_room.html',context)