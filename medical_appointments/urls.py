"""
URL configuration for medical_appointments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home_view, authentication_view, verify_view, register_view, dashboard_view, profile_view, \
    logout_view, service_view, doctors_pediatric_view, success_page_view, make_appointment_view, DoctorCalendarView, \
    patient_appointments_view, doctors_cardiologist_view, doctors_internal_medicine_view, \
    doctors_general_medicine_view, doctors_gastroenterologist_view, doctors_psychologist_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home-view'),
    path('authentication/', authentication_view, name='authentication-view'),
    path('dashboard/logout/', logout_view, name='logout-view'),
    path('authentication/verify/', verify_view, name='verify-view'),
    path('register/', register_view, name='register-view'),
    path('authentication/verify/dashboard/', dashboard_view, name='dashboard-view'),
    path('profile/', profile_view, name='profile-view'),
    path('service/', service_view, name='service-view'),
    path('doctors_pediatric/', doctors_pediatric_view, name='doctors-pediatric-view'),
    path('doctors_cardiologist/', doctors_cardiologist_view, name='doctors-cardiologist-view'),
    path('doctors_internal_medicine/', doctors_internal_medicine_view, name='doctors-internal-medicine-view'),
    path('doctors_gastroenterologist/', doctors_gastroenterologist_view, name='doctors-gastroenterologist-view'),
    path('doctors_general_medicine/', doctors_general_medicine_view, name='doctors-general-medicine-view'),
    path('doctors_psychologist/', doctors_psychologist_view, name='doctors-psychologist-view'),



    path('doctors_pediatric/<int:doctor_id>/', make_appointment_view, name='make-appointment-view'),
    path('doctors_cardiologist/<int:doctor_id>/', make_appointment_view, name='make-appointment-view'),
    path('doctors_internal_medicine/<int:doctor_id>/', make_appointment_view, name='make-appointment-view'),
    path('doctors_gastroenterologist/<int:doctor_id>/', make_appointment_view, name='make-appointment-view'),
    path('doctors_general_medicine/<int:doctor_id>/', make_appointment_view, name='make-appointment-view'),
    path('doctors_psychologist/<int:doctor_id>/', make_appointment_view, name='make-appointment-view'),


    path('success/', success_page_view, name='success-page-view'),
    path('<int:doctor_id>/calendar/', DoctorCalendarView.as_view(), name='doctor_calendar'),
    path('patient_appointments/', patient_appointments_view, name='patient-appointments-view'),
]
