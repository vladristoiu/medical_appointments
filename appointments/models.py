from django.db import models
from django.contrib.auth.models import AbstractUser
import random


ConsultationType = [
    ('Pediatric consultation', 'Pediatric consultation'),
    ('Cardiology consultation', 'Cardiology consultation'),
    ('Internal medicine consultation', 'Internal medicine consultation'),
    ('Gastroenterology consultation', 'Gastroenterology consultation'),
    ('General medicine consultation', 'General medicine consultation'),
    ('Psychological consultation', 'Psychological consultation')

]


class Patient(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    adress = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"


class Doctor(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, choices=ConsultationType, default='General medicine consultation')
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    duration = models.IntegerField(default=1, editable=False)
    status = models.CharField(max_length=100, editable=False, default='Pending')

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name}'s appointment with Dr. {self.doctor.first_name} \
        {self.doctor.last_name} on {self.date} at {self.time}"


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.DateField()

    def __str__(self):
        return f"Schedule for Dr. {self.doctor.first_name} {self.doctor.last_name} on {self.day_of_week} "


class Token(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        number_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        token_items = []

        for i in range(5):
            x = random.choice(number_list)
            token_items.append(x)

        token_string = "".join(str(item) for item in token_items)
        self.number = token_string
        super().save(*args, **kwargs)
