from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import InsertForm


def insert_data(request):
    form = InsertForm(request.POST or None)
    status = ''
    if form.is_valid():
        response = form.insert()
        if response.status_code == 201:
            form.notify_remotes()
            status = 'Success with 201'
            messages.success(request, status)
            return redirect('insert')
        else:
            status = 'Query failed with code %s' % response.status_code
    context = {
        'form': form,
        'status': status,
    }
    return render(request, 'virtuoso/insert.html', context)
