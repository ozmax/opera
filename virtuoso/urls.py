from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/triple', views.add_triple, name='virtuoso_add_triple'),
]
