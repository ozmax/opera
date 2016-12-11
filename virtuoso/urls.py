from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^insert/$', views.insert_data, name='insert'),
]
