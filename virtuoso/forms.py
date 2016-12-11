from django import forms

from .utils import make_query, get_triplets, send_notif, \
    REGISTERED_ENDPOINTS


class InsertForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    query = forms.CharField(widget=forms.Textarea)

    def insert(self):
        response = make_query(self.cleaned_data)
        return response

    def notify_remotes(self):
        triplets = get_triplets(self.cleaned_data['query'])
        for triple in triplets:
            if triple[0] in REGISTERED_ENDPOINTS:
                send_notif(triple[0])
            if triple[2] in REGISTERED_ENDPOINTS:
                send_notif(triple[2])
