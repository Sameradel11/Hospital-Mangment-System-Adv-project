from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Patient(models.Model):
    PatientID = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    DOB = models.DateField()
    Gender = models.CharField(max_length=10)
    Address = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.FullName

class Doctor(models.Model):
    specializationList=['Cardiology','Dermatology','Neurology','Orthopedics',
    'Ophthalmology','Oncology','Psychiatry','Pediatrics']
    DoctorID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Specialization = models.CharField(max_length=100)
    def __str__(self):
        return self.Name

class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    Required_Specialization = models.CharField(max_length=100)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.PatientID.FullName} Appointment'

class Treatment(models.Model):
    TreatmentID = models.AutoField(primary_key=True)
    ProcedureDescription = models.TextField()
    AppointmentID = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.TreatmentID)

class Room(models.Model):
    RoomNumber = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=50)
    Availability = models.BooleanField()
    def __str__(self):
        return str(self.RoomNumber)

class Admission(models.Model):
    AdmissionID = models.AutoField(primary_key=True)
    AdmissionDate = models.DateField(auto_now_add=True)
    Reason = models.CharField(max_length=255,null=True)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    RoomNumber = models.ForeignKey(Room, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.PatientID.FullName)

class StayDetails(models.Model):
    StayDetailsID = models.AutoField(primary_key=True)
    Date = models.DateField(auto_now_add=True)
    AdmissionID = models.ForeignKey(Admission, on_delete=models.CASCADE)

class Discharge(models.Model):
    DischargeID = models.AutoField(primary_key=True)
    DischargeDate = models.DateField(auto_now_add=True)
    Reason = models.CharField(max_length=255)
    AdmissionID = models.ForeignKey(Admission, on_delete=models.CASCADE)

class Patient_ContactDetails(models.Model):
    ContactDetails = models.CharField(max_length=100, primary_key=True)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)

class Doctor_ContactDetails(models.Model):
    ContactDetails = models.CharField(max_length=100, primary_key=True)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)


class StayDetails_Meals(models.Model):
    dateadded = models.DateTimeField(primary_key=True,auto_now_add=True)
    Meals = models.CharField(max_length=100)
    StayDetailsID = models.ForeignKey('StayDetails', on_delete=models.CASCADE)

class StayDetails_AdministeredTreatments(models.Model):
    dateadded = models.DateTimeField(primary_key=True, auto_now_add=True)
    AdministeredTreatments = models.CharField(max_length=255)
    StayDetailsID = models.ForeignKey('StayDetails', on_delete=models.CASCADE)

class StayDetails_ConditionUpdates(models.Model):
    dateadded = models.DateTimeField(primary_key=True, auto_now_add=True)
    ConditionUpdates = models.CharField(max_length=255)
    StayDetailsID = models.ForeignKey('StayDetails', on_delete=models.CASCADE)

class Treatment_TestResults(models.Model):
    dateadded = models.DateTimeField(primary_key=True, auto_now_add=True)
    TestResults = models.CharField(max_length=100)
    TreatmentID = models.ForeignKey('Treatment', on_delete=models.CASCADE)

class Treatment_Medications(models.Model):
    dateadded = models.DateTimeField(primary_key=True, auto_now_add=True)
    Medications = models.CharField(max_length=100)
    TreatmentID = models.ForeignKey('Treatment', on_delete=models.CASCADE)
    def __str__(self):
        return self.Medications
    
