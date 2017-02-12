from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^select$', views.select, name='virtuoso_select'),
    url(r'^insert$', views.insert, name='virtuoso_insert'),
]
