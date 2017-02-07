from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import InsertForm


def query_data(request):
    form = InsertForm(request.POST or None, request.FILES or None)
    status = ''
    if form.is_valid():
        response = form.virtuoso_insert()
        if response.status_code == 201:
            form.create_notifications()
            status = 'Success with 201'
            messages.success(request, status)
            return redirect('insert')
        else:
            status = 'Query failed with code %s' % response.status_code
            messages.error(request, status)
    context = {
        'form': form,
    }
    return render(request, 'virtuoso/insert.html', context)
