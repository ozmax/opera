import requests

from django import forms

from .conf import MY_ENDPOINT, REGISTERED_ENDPOINTS, HEADERS, VIRTUOSO_ENDPOINT
from .utils import get_triplets, send_notif


class InsertForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    query = forms.CharField(widget=forms.Textarea, required=False)
    upload = forms.FileField(required=False)

    def clean(self):
        data = self.cleaned_data
        if (data.get('query') and data.get('upload') or
                (not data.get('query') and not data.get('upload'))):
            raise forms.ValidationError('Fill query OR file')
        return data

    def insert(self):
        response = make_query(self.cleaned_data)
    def virtuoso_insert(self):
        data = self.cleaned_data
        username = data.get('username', '')
        password = data.get('password', '')
        query = data.get('query', '')
        file_query = data.get('upload', '')
        data = query if query else file_query
        headers = HEADERS['sparql_query']

        response = requests.post(
            url=VIRTUOSO_ENDPOINT,
            headers=headers,
            auth=(username, password),
            data=data
        )
        return response

    def notify_remotes(self):
        data = self.cleaned_data

        if data.get('upload'):
            data_string = ''
            for line in data['upload']:
                data_string += line

        else:
            data_string = data['query']

        triplets = get_triplets(data_string)
        for triple in triplets:
            subject, predicate, obj = triple
            for endpoint in REGISTERED_ENDPOINTS.keys():
                if endpoint in subject:
                    username = REGISTERED_ENDPOINTS[endpoint]['username']
                    password = REGISTERED_ENDPOINTS[endpoint]['password']

                    send_notif(
                        username, password, MY_ENDPOINT, subject, predicate,
                    )
