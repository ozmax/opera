import requests

from django.conf import settings

from celery import shared_task

from virtuoso.conf import MY_ENDPOINT
from .models import NotificationRequest


@shared_task(autoretry_for=(requests.ConnectionError,),
             retry_kwargs={'max_retries': settings.MAX_RETRIES},
             default_retry_delay=(settings.RETRY_DELAY))
def notify_remote(notif_id):
    notif = NotificationRequest.objects.get(id=notif_id)
    data = {
        'username': notif.remote.username,
        'password': notif.remote.password,

        'source': MY_ENDPOINT,
        'resource': notif.resource,
        'predicate': notif.predicate,
    }

    url = '%strends/notify/' % notif.remote.url

    r = requests.post(url, data)
    if r.ok:
        notif.complete = True
        notif.save()
