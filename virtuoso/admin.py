from django.contrib import admin

from .models import RemoteServer, NotificationRequest


@admin.register(RemoteServer)
class RemoteServerAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationRequest)
class NotificationRequestAdmin(admin.ModelAdmin):
    # list
    list_display = ['remote', 'resource', 'predicate', 'complete']
