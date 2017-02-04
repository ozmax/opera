import requests

from django import forms
from django.conf import settings

from .models import RemoteServer, NotificationRequest
from .parser import parse_query
from .tasks import notify_remote


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

    def virtuoso_insert(self):
        headers = {'Content-Type': 'application/sparql-query'}

        data = self.cleaned_data
        username = data.get('username', '')
        password = data.get('password', '')
        query = data.get('query', '')
        file_query = data.get('upload', '')
        data = query if query else file_query

        response = requests.post(
            url=settings.VIRTUOSO_ENDPOINT,
            headers=headers,
            auth=(username, password),
            data=data
        )
        return response

    def create_notifications(self):
        # get parsed query
        data = self.cleaned_data
        if data.get('upload'):
            query = ''
            for line in data['upload']:
                query += line
        else:
            query = data['query']

        records = parse_query(query)

        servers = RemoteServer.objects.all()
        for record in records:
            subject, predicate, obj = record

            for server in servers:
                if server.url in subject:
                    notif = NotificationRequest.objects.create(
                        remote=server,
                        resource=subject,
                        predicate=predicate,
                    )
                    notify_remote.delay(notif.pk)
                if server.url in obj:
                    NotificationRequest.objects.create(
                        remote=server,
                        resource=obj,
                        predicate=predicate,
                    )
                    notify_remote.delay(notif.pk)
