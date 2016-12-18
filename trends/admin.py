from django.contrib import admin

from .models import Resource, Endpoint, Backlink


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    pass


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Backlink)
class BacklinkAdmin(admin.ModelAdmin):
    pass
