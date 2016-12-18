from __future__ import unicode_literals

from django.db import models


class Resource(models.Model):
    uri = models.CharField(max_length=255)

    def __unicode__(self):
        return self.uri


class Endpoint(models.Model):
    uri = models.CharField(max_length=255)

    def __unicode__(self):
        return self.uri


class Backlink(models.Model):
    resource = models.ForeignKey(Resource)
    endpoint = models.ForeignKey(Endpoint)
    predicate = models.CharField(max_length=255)
    count = models.IntegerField(default=1)

