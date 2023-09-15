from django.test import TestCase
import timeit
from appointments.models import Doctor, Patient, Appointment
from datetime import datetime


class TestDatabaseSpeed(TestCase):

    def setUp(self):
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Deer",
            domain="General medicine",
            email="agdab@gmail.com",
            phone_number="+4073635252",


        )

        self.patient = Patient.objects.create(
            username="testuser",
            password="testpass",
            email="jadgjad@gmail.com",
            birth_date="2000-11-11",
            phone_number="+407352627",
            adress="Strada Da"

        )

    def test_create_appointment(self):
        def create_appointment():
            Appointment.objects.create(
                doctor=self.doctor,
                patient=self.patient,
                date=datetime.now(),
                time="09:00"

            )

        elapsed_time = timeit.timeit(create_appointment, number=10000)
        print(f"Time taken to create 100 appointments: {elapsed_time} seconds")

        self.assertLess(elapsed_time, 3)
