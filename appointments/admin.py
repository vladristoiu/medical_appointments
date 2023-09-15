from django.contrib import admin
from .models import Token, Patient, Doctor, DoctorSchedule, Appointment
from django.contrib.auth.models import Group


admin.site.register(Token)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(DoctorSchedule)
admin.site.unregister(Group)
