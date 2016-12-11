from django import forms

from .utils import make_query


class InsertForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    query = forms.CharField(widget=forms.Textarea)

    def insert(self):
        response = make_query(self.cleaned_data)
        return response
