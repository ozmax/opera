from .models import Backlink, Resource, Endpoint


def save_resource(endpoint, resource, predicate):
    try:
        endpoint = Endpoint.objects.get(uri=endpoint)
    except Endpoint.DoesNotExist:
        endpoint = Endpoint.objects.create(uri=endpoint)


    try:
        resource = Resource.objects.get(uri=resource)
    except Resource.DoesNotExist:
        resource = Resource.objects.create(uri=resource)


    try:
        backlink = Backlink.objects.get(
            endpoint=endpoint, resource=resource, predicate=predicate
        )
        backlink.count += 1
        backlink.save()
    except Backlink.DoesNotExist:
        backlink = Backlink.objects.create(
            endpoint=endpoint, resource=resource, predicate=predicate
        )

    return backlink
