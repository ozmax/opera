import requests


HEADERS = {
    'sparql_query': {'Content-Type': 'application/sparql-query'},
}

VIRTUOSO_ENDPOINT = 'http://83.212.116.88:8890/DAV/xx/demo'


def create_sparql_insert_query(uri1, uri2, uri3):
    query = 'INSERT {<%s> <%s> <%s>}'
    return query % (uri1, uri2, uri3)


def insert_triple(data):
    username = data.get('username', '')
    password = data.get('password', '')
    uri1 = data.get('uri1', '')
    uri2 = data.get('uri2', '')
    uri3 = data.get('uri3', '')

    headers = HEADERS['sparql_query']

    response = requests.post(
        url=VIRTUOSO_ENDPOINT,
        headers=headers,
        auth=(username, password),
        data=create_sparql_insert_query(uri1, uri2, uri3)
    )
    return response
