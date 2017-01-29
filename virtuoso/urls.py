from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('insert')),
        name='redirect_insert'),
    url(r'^insert/$', views.insert_data, name='insert'),
]
