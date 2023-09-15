from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from appointments.forms import TokenForm, NewUserForm, AppointmentForm
from appointments.models import Patient, Doctor, Appointment,  DoctorSchedule, Token
from datetime import date, datetime
from django.db import transaction


def home_view(request):
    return render(request, 'main.html', {})


def authentication_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify-view')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'authentication.html', {'form': form})


@transaction.atomic
def verify_view(request):
    form = TokenForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = Patient.objects.get(pk=pk)
        token = user.token
        token_user = f"{user.username}: {user.token}"
        if not request.POST:

            print(token_user)
            send_verification_email(user.email, token, user.username)

        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(token) == num:
                token.save()
                login(request, user)
                return redirect('dashboard-view')
            else:
                form.add_error('number', 'The entered code is incorrect.')
    if not pk:
        return redirect('authentication-view')
    return render(request, 'verify.html', {'form': form})


def send_verification_email(patient_email, token, user_username):
    subject = 'Verification Code'
    message = f'Hello {user_username}, \n\nYour verification code is {token}.'
    email_from = 'behealthy1957@gmail.com'
    recipient_list = [patient_email]
    send_mail(subject, message, email_from, recipient_list)


def logout_view(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out.")
    return redirect('home-view')


@transaction.atomic
def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Token.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home-view")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()

    return render(request, "register.html", {"register_form": form})


@login_required
def dashboard_view(request):
    return render(request, 'newbase.html', {})


@transaction.atomic
def profile_view(request):
    user = request.user
    if isinstance(user, Patient):
        if request.method == 'POST':

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.birth_date = request.POST.get('birth_date')
            user.adress = request.POST.get('adress')
            user.phone_number = request.POST.get('phone_number')
            user.email = request.POST.get('email')
            user.save()

        context = {'user': user}
        return render(request, 'profile.html', context)


def service_view(request):
    return render(request, 'service.html', {})


def doctors_pediatric_view(request):
    doctors = Doctor.objects.filter(domain='Pediatric consultation')
    return render(request, 'pediatric_doctors.html', {'doctors': doctors})


def doctors_cardiologist_view(request):
    doctors = Doctor.objects.filter(domain='Cardiology consultation')
    return render(request, 'cardiology_doctors.html', {'doctors': doctors})


def doctors_internal_medicine_view(request):
    doctors = Doctor.objects.filter(domain='Internal medicine consultation')
    return render(request, 'internal_medicine_doctors.html', {'doctors': doctors})


def doctors_gastroenterologist_view(request):
    doctors = Doctor.objects.filter(domain='Gastroenterology consultation')
    return render(request, 'gastroenterology_doctors.html', {'doctors': doctors})


def doctors_general_medicine_view(request):
    doctors = Doctor.objects.filter(domain='General medicine consultation')
    return render(request, 'general_medicine_doctors.html', {'doctors': doctors})


def doctors_psychologist_view(request):
    doctors = Doctor.objects.filter(domain='Psychological consultation')
    return render(request, 'psychological_doctors.html', {'doctors': doctors})


def send_confirmation_email(patient_email, doctor_name, appointment_date, appointment_time, patient_name):
    subject = 'Appointment Confirmation'
    message = f'Hello {patient_name},You have an appointment with Dr. {doctor_name} on ' \
              f'{appointment_date}, starting at {appointment_time}. \n\nBest regards,\nBeHealthy Clinic'
    email_from = 'behealthy1957@gmail.com'
    recipient_list = [patient_email]
    send_mail(subject, message, email_from, recipient_list)


@transaction.atomic
def make_appointment_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, initial={'doctor_id': doctor.id})
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user
            appointment.save()

            doctor_name = f"{doctor.first_name} {doctor.last_name}"
            patient_name = f"{request.user.first_name} {request.user.last_name}"
            send_confirmation_email(
                patient_email=request.user.email,
                patient_name=patient_name,
                doctor_name=doctor_name,
                appointment_date=appointment.date,
                appointment_time=appointment.time
            )

            return redirect('success-page-view')
    else:
        form = AppointmentForm(initial={'doctor_id': doctor.id})
    return render(request, 'make_appointment.html', {'form': form, 'doctor': doctor})


def success_page_view(request):
    return render(request, 'success.html')


class DoctorCalendarView(TemplateView):
    template_name = "doctor_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        doctor_id = self.kwargs.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        current_date = date.today()

        schedules = DoctorSchedule.objects.filter(doctor=doctor, day_of_week__gte=current_date).\
            order_by('day_of_week', 'start_time')

        appointments = Appointment.objects.filter(doctor=doctor, date__gte=current_date).order_by('date', 'time')

        context['schedules'] = schedules
        context['appointments'] = appointments
        context['doctor'] = doctor

        return context


def patient_appointments_view(request):
    if request.user.is_authenticated:

        all_appointments = Appointment.objects.filter(patient=request.user).order_by('date', 'time')

        current_date = date.today()
        current_time = datetime.now().time()

        pending_appointments = []
        completed_appointments = []

        for appointment in all_appointments:
            if appointment.date > current_date or (
                    appointment.date == current_date and appointment.time > current_time):
                appointment.status = "Pending"
                pending_appointments.append(appointment)
            else:
                appointment.status = "Completed"
                completed_appointments.append(appointment)
            appointment.save()
        context = {
            'pending_appointments': pending_appointments,
            'completed_appointments': completed_appointments
        }
        return render(request, 'patient_appointments.html', context)
