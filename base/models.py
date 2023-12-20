from django.db import models

class Patient(models.Model):
    Patient_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Address = models.CharField(max_length=100)
    Phone_Number = models.CharField(max_length=14)
    Date_Of_Birth = models.DateField()

    def __str__(self):
        return f"Patient ID: {self.Patient_ID}, Name: {self.Name}"

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        'Cardiologist',
        'Dermatologist',
        'Neurologist',
        'Pediatrician',
        'Ophthalmologist',
        'Orthopedic Surgeon',
        'Gynecologist',
        'ENT Specialist',
        'Psychiatrist',
        'Urologist',
    ]
    Doctor_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Specialization = models.CharField(max_length=20)
    Phone_Number = models.CharField(max_length=14)
    Appointment_Price = models.IntegerField()

    def __str__(self):
        return f"Doctor ID: {self.Doctor_ID}, Name: {self.Name}"

class Appointment(models.Model):
    Appointment_ID=models.AutoField(primary_key=True)
    Date = models.DateTimeField(auto_now_add=True)
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    def __str__(self):
        return f"Patient: {self.Patient_ID.Name}|Doctor: {self.Doctor_ID.Name}|Specialization: {self.Doctor_ID.Specialization}"

class Treatment(models.Model):
    Treatment_ID = models.AutoField(primary_key=True)
    Procedure = models.CharField(max_length=255)
    Disease = models.CharField(max_length=255)
    Appointment_ID = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return f"Treatment ID: {self.Treatment_ID}, Procedure: {self.Procedure}, Disease: {self.Disease}"

class Room(models.Model):
    Room_ID=models.AutoField(primary_key=True)
    Room_Number = models.CharField(max_length=20)
    Room_Type = models.CharField(max_length=20)
    Room_Price = models.IntegerField()
    def __str__(self):
        return f"Room Number: {self.Room_Number}, Type: {self.Room_Type}"

class Bill(models.Model):
    Bill_ID = models.AutoField(primary_key=True)
    Date = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=10)
    Total = models.IntegerField()
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Reason=models.CharField(max_length=255,default="Reason")
    def __str__(self):
        return f"Bill ID: {self.Bill_ID}, Total: {self.Total}"

class Employee(models.Model):
    Employee_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Phone_Number = models.CharField(max_length=14)
    Role = models.CharField(max_length=255)
    def __str__(self):
        return f"Employee ID: {self.Employee_ID}, Name: {self.Name}"

class Employee_Room(models.Model):
    Employee_ID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Room_Number = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('Employee_ID', 'Room_Number')

    def __str__(self):
        return f"Employee ID: {self.Employee_ID}, Room Number: {self.Room_Number}"
from django.utils import timezone

class Admission(models.Model):
    Admission_ID = models.AutoField(primary_key=True)
    Start_Date = models.DateTimeField(default=timezone.now)
    End_Date = models.DateTimeField(null=True)
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Room_Number = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admission ID: {self.Admission_ID}, Start Date: {self.Start_Date}"

class TreatmentAdmission(models.Model):
    Treatment_ID = models.AutoField(primary_key=True)
    Treatment_Title = models.CharField(max_length=255)
    Treatment_Details = models.TextField(max_length=255)
    DateTime = models.DateTimeField(auto_now_add=True)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    price=models.IntegerField()
    def __str__(self):
        return f"Treatment ID: {self.Treatment_ID}, Title: {self.Treatment_Title}"
