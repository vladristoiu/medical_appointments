from django import forms
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from .models import Token
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Appointment, DoctorSchedule


class TokenForm(forms.ModelForm):
    number = forms.CharField(label='Token', help_text='Enter the code for verification')

    class Meta:
        model = Token
        fields = ('number',)

    def clean_number(self):
        number = self.cleaned_data.get('number')
        return number


class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True)
    birth_date = forms.DateField(required=True)
    adress = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Patient
        fields = ("username", "first_name", "last_name", "email", "adress", "phone_number", "birth_date")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if Patient.objects.filter(username=username).exists():
            raise ValidationError("Username already exists, please choose another one.")

        return username

    def save(self, commit=True):
        patient = super(NewUserForm, self).save(commit=False)
        patient.email = self.cleaned_data['email']
        patient.adress = self.cleaned_data['adress']
        patient.phone_number = self.cleaned_data['phone_number']
        patient.birth_date = self.cleaned_data['birth_date']
        patient.first_name = self.cleaned_data['first_name']
        patient.last_name = self.cleaned_data['last_name']

        if commit:
            patient.save()
        return patient


def time_intervals_overlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['time', 'date']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        doctor_id = self.initial.get('doctor_id')
        current_datetime = datetime.now()

        chosen_datetime = datetime.combine(date, time)
        if chosen_datetime < current_datetime:
            raise forms.ValidationError("You cannot book appointments in the past.")

        doctor_schedules = DoctorSchedule.objects.filter(doctor_id=doctor_id, day_of_week=date)
        duration = 1
        for schedule in doctor_schedules:

            latest_possible_time = (datetime.combine(date, schedule.end_time) - timedelta(hours=duration)).time()
            if schedule.start_time <= time <= latest_possible_time:
                break
        else:
            raise forms.ValidationError("Doctor is not available at the chosen time.")

        combined_datetime = datetime.combine(date, time)
        appointment_end_datetime = combined_datetime + timedelta(hours=1)
        appointment_end_time = appointment_end_datetime.time()

        existing_appointments = Appointment.objects.filter(doctor_id=doctor_id, date=date)
        for existing_appointment in existing_appointments:
            existing_end_datetime = datetime.combine(date, existing_appointment.time) + timedelta(
                hours=existing_appointment.duration)
            existing_end_time = existing_end_datetime.time()
            if time_intervals_overlap(time, appointment_end_time, existing_appointment.time, existing_end_time):
                raise ValidationError("Doctor already has an appointment in the chosen time range.")

        return cleaned_data
