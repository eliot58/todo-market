from celery import shared_task
from .models import Provider

@shared_task
def reset_status(provider_id):
    provider = Provider.objects.get(id=provider_id)