from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import InsertForm, SelectForm


def home(request):
    insert_form = InsertForm()
    select_form = SelectForm()

    context = {
        'insert_form': insert_form,
        'select_form': select_form,
        'active_form': 'insert',
    }
    return render(request, 'virtuoso/home.html', context)


def select(request):
    select_form = SelectForm(request.POST, request.FILES)
    if select_form.is_valid():
        response, should_download, ext = select_form.virtuoso_select()
        if response.ok:
            if should_download:
                response = HttpResponse(
                    response.text,
                    content_type=should_download
                )
                response['Content-Disposition'] = (
                    'attachment; filename=select.%s' % ext
                )
                return response
            else:
                return render(request, 'virtuoso/results.html', {
                    'results': response.text,
                })
        else:
            status = 'Query failed with code %s' % response.status_code
            messages.error(request, status)
    context = {
        'select_form': select_form,
        'insert_form': InsertForm(),
        'active_form': 'select'
    }
    return render(request, 'virtuoso/home.html', context)


def insert(request):
    insert_form = InsertForm(request.POST or None, request.FILES or None)
    if insert_form.is_valid():
        response = insert_form.virtuoso_insert()
        status = ''
        if response.status_code == 201:
            insert_form.create_notifications()
            status = 'Success with 201'
            messages.success(request, status)
            return redirect('home')
        else:
            status = 'Query failed with code %s' % response.status_code
            messages.error(request, status)
    context = {
        'insert_form': insert_form,
        'select_form': SelectForm(),
        'active_form': 'insert'
    }
    return render(request, 'virtuoso/home.html', context)
