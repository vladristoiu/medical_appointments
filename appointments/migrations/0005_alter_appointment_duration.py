# Generated by Django 4.2.1 on 2023-08-31 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_alter_appointment_status_alter_doctor_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='duration',
            field=models.IntegerField(default=1, editable=False),
        ),
    ]
