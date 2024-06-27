from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Provider

@shared_task
def reset_status():
    providers = Provider.objects.filter(status_time__date=timezone.now().date())

    for provider in providers:
        provider.status = "free"
        provider.status_time = None


    provider.save()



@shared_task
def send_status_notification():
    providers = Provider.objects.filter(status_time__date=timezone.now().date() + timedelta(days=3))

    for provider in providers:
        send_mail(
            "Статус",
            f"До окончания статуса {provider.get_status_display()} осталось 3 дня",
            settings.EMAIL_HOST_USER,
            [provider.email],
            fail_silently=False
        )