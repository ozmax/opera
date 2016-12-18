from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_http_methods

from .forms import NotificationForm
from django.contrib.auth.decorators import login_required


@csrf_exempt
@require_http_methods(['POST',])
def notify(request):
    form = NotificationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse(status=201)

    return HttpResponse(status=405)
