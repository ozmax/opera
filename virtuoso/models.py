from django.db import models


class RemoteServer(models.Model):
    url = models.URLField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __unicode__(self):
        return self.url


class NotificationRequest(models.Model):
    remote = models.ForeignKey(RemoteServer)
    resource = models.CharField(max_length=255)
    predicate = models.CharField(max_length=255)

    complete = models.BooleanField(default=False)
