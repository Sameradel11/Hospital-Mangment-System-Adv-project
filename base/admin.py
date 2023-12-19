from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Treatment)
admin.site.register(Treatment_Medications)
admin.site.register(Discharge)
admin.site.register(StayDetails)
admin.site.register(StayDetails_AdministeredTreatments)
admin.site.register(StayDetails_ConditionUpdates)
admin.site.register(StayDetails_Meals)






