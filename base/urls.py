from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('add_patient/',views.add_patient,name='add_patient'),
    path('doctors/',views.doctor,name='doctors'),
    path('add_doctor/',views.add_doctor,name='add_doctor'),
    path('add_appointment/',views.add_appointment,name='add_appointment'),
    path('remove_patient/<str:pk>',views.remove_patient,name='remove_patient'),
    path('remove_doctor/<str:pk>',views.remove_doctor,name='remove_doctor'),
    path('edit_patient/<str:pk>',views.edit_patient,name='edit_patient'),
    path('edit_doctor/<str:pk>',views.edit_doctor,name='edit_doctor'),
    path('remove_appointment/<str:pk>',views.remove_appointment,name='remove_appointment'),
    path('admission/',views.admission,name='admission'),
    path('appointment/',views.appointment,name='appointment'),
    path('discharge/', views.discharge, name='discharge'),
    path('patient/', views.patient, name='patient'),
    path('room/', views.room, name='room'),
    path('add_room/',views.add_room,name='add_room'),
    path('remove_room/<str:pk>',views.remove_room,name='remove_room'),
    path('start/', views.start, name='start'),
    # path('staydetails/', views.staydetails, name='staydetails'),
    path('treatment/', views.treatment, name='treatment'),
    path('remove_treatment/<str:pk>', views.remove_treatment, name='remove_treatment'),
    # path('medication/<str:pk>',views.medication,name='medication'),
    path('add_admission/<str:pk>',views.add_admission,name='add_admission'),
    path('remove_admission/<str:pk>',views.remove_admission,name='remove_admission'),
    path('add_treatment/<str:pk>',views.add_treatment,name='add_treatment'),
    path('add_discharge/<str:pk>',views.add_discharge,name='add_discharge'),
    # path('add_medicine/<str:pk>',views.add_medicine,name='add_medicine'),
    path('remove_discharge/<str:pk>',views.remove_discharge,name='remove_discharge'),
    path('add_admin_treatment/<str:pk>', views.add_admin_tratment,name='add_admin_treatment'),
    # path('add_condition_update/<str:pk>', views.add_condition_update,name='add_condition_update'),
    # path('add_meal/<str:pk>', views.add_meal,name='add_meal'),
    # path('add_staydetails/<str:pk>',views.add_staydetails,name='add_staydetails'),
    # path('remove_staydetails/<str:pk>',views.remove_staydetails,name='remove_staydetails'),
    path('edit_room/<str:pk>',views.edit_room,name='edit_room'),
    path('admission_treatments/<str:pk>',views.admission_treatments,name='admission_treatments'),
    path('bill/<str:pk>',views.bill,name='bill'),
    path('remove_admission_treatment/<str:pk>',views.remove_admission_treatment,name='remove_admission_treatment')
    ,path('pay_bill/<str:pk>',views.paybill,name='pay_bill')
    ,path('add_employee',views.add_employee,name='add_employee')
    ,path('remove_employee,<str:pk>',views.remove_employee,name='remove_employee')
    ,path('employee',views.employee,name='employee')
    ,path('add_employee_room/<str:pk>',views.add_employee_room,name='add_employee_room')
]
