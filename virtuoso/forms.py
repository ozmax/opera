from django import forms

from .utils import MY_ENDPOINT, REGISTERED_ENDPOINTS, get_triplets, \
    make_query, send_notif


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
        return response

    def notify_remotes(self):
        triplets = get_triplets(self.cleaned_data['query'])
        for triple in triplets:
            subject, predicate, obj = triple
            for endpoint in REGISTERED_ENDPOINTS.keys():
                if endpoint in subject:
                    username = REGISTERED_ENDPOINTS[endpoint]['username']
                    password = REGISTERED_ENDPOINTS[endpoint]['password']

                    send_notif(
                        username, password, MY_ENDPOINT, subject, predicate,
                    )
