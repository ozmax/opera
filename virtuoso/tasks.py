import requests

from celery import shared_task

from virtuoso.conf import MY_ENDPOINT
from .models import NotificationRequest


@shared_task(autoretry_for=(requests.ConnectionError,),
             retry_kwargs={'max_retries': 5},
             default_retry_delay=10)
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
