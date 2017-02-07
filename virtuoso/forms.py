import requests

from django import forms
from django.conf import settings

from .models import RemoteServer, NotificationRequest
from .parser import parse_query
from .tasks import notify_remote


class QueryBaseForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea, required=False)
    upload = forms.FileField(required=False)

    def clean(self):
        data = self.cleaned_data
        if (data.get('query') and data.get('upload') or
                (not data.get('query') and not data.get('upload'))):
            raise forms.ValidationError('Fill query OR file')
        return data


class SelectForm(QueryBaseForm):

    DOWNLOAD_CHOICES = [
        ('auto', 'Auto'),
        ('application/vnd.ms-excel', 'Spreadsheet'),
        ('application/sparql-results+xml', 'XML'),
        ('text/csv', 'CSV'),
        ('text/tab-separated-values', 'TSV'),
        ('application/rdf+xml', 'RDF/XML'),
    ]

    NEW_PAGE_CHOICES = [
        ('text/html', 'HTML'),
        ('application/sparql-results+json', 'JSON'),
        ('application/javascript', 'Javascript'),
        ('text/plain', 'NTriples'),
    ]

    extensions = {
        'auto': 'xml',
        'application/vnd.ms-excel': 'xls',
        'application/sparql-results+xml': 'xml',
        'text/csv': 'csv',
        'text/tab-separated-values': 'tsv',
        'application/rdf+xml': 'xml',
    }

    response_type = forms.ChoiceField(
        choices=DOWNLOAD_CHOICES + NEW_PAGE_CHOICES,
    )

    def virtuoso_select(self):
        url = settings.VIRTUOSO_SPARQL_ENDPOINT

        data = self.cleaned_data
        format_type = data['response_type']
        query = data.get('query', '')
        file_query = data.get('upload', '')
        query_string = query if query else file_query

        params = {
            'query': query_string,
            'format': format_type,
        }
        response = requests.get(url=url, params=params)

        # return the response and if the view should return a page or a file
        for choice in self.DOWNLOAD_CHOICES:
            if format_type in choice[0]:
                should_download = format_type
                ext = self.extensions[format_type]
                break
            else:
                should_download = None
                ext = None
        return response, should_download, ext


class InsertForm(QueryBaseForm):
    username = forms.CharField(initial='demo')
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        initial='demo'
    )
    query = forms.CharField(widget=forms.Textarea, required=False)
    upload = forms.FileField(required=False)

    def virtuoso_insert(self):
        headers = {'Content-Type': 'application/sparql-query'}

        data = self.cleaned_data
        username = data.get('username', '')
        password = data.get('password', '')
        query = data.get('query', '')
        file_query = data.get('upload', '')
        data = query if query else file_query

        response = requests.post(
            url=settings.VIRTUOSO_INSERT_ENDPOINT,
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
