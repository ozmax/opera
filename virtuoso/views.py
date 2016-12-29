from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import InsertForm


def insert_data(request):
    form = InsertForm(request.POST or None, request.FILES or None)
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
