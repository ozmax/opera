from django import forms
from django.contrib.auth import authenticate, login

from .utils import save_resource

class NotificationForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    source = forms.CharField(max_length=255)
    resource = forms.CharField(max_length=255)
    predicate = forms.CharField(max_length=255)


    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if authenticate(username=username, password=password):
            source = self.cleaned_data.get('source')
            resource = self.cleaned_data.get('resource')
            predicate = self.cleaned_data.get('predicate')
            result = save_resource(source, resource, predicate)
            return result
        else:
            print 'Nope'
