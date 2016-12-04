from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .utils import insert_triple


@csrf_exempt
@require_http_methods(['POST'])
def add_triple(request):
    data = request.POST
    response = insert_triple(data)
    django_response = HttpResponse(status=response.status_code)
    return django_response
