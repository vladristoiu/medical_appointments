from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from appointments.models import Appointment
from datetime import date


def send_appointment_reminders():

    today_appointments = Appointment.objects.filter(date=date.today())
    for appointment in today_appointments:
        patient_email = appointment.patient.email
        doctor_name = f"Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}"
        subject = "Reminder for your appointment today"
        message = f"Hello {appointment.patient.first_name},\n\nYou have an appointment scheduled with " \
                  f"{doctor_name} at {appointment.time} today. Please make sure to be on time.\n\nBest regards," \
                  f"\nBeHealthy Clinic"

        send_mail(
            subject,
            message,
            'behealthy1967@gmail.com',
            [patient_email],
            fail_silently=False,
        )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_appointment_reminders, 'cron', day_of_week='mon-sun', hour=9,
                      minute=30)
    scheduler.start()