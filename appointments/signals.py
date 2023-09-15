from appointments.models import Patient
from appointments.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
'''
@receiver(post_save, sender=Patient)
def post_save_generate_token(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)
'''