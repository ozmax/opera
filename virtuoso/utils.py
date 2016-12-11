import requests


HEADERS = {
    'sparql_query': {'Content-Type': 'application/sparql-query'},
}

VIRTUOSO_ENDPOINT = 'http://83.212.116.88:8890/DAV/xx/demo'


def make_query(data):
    username = data.get('username', '')
    password = data.get('password', '')
    query = data.get('query', '')

    headers = HEADERS['sparql_query']

    response = requests.post(
        url=VIRTUOSO_ENDPOINT,
        headers=headers,
        auth=(username, password),
        data = query
    )
    return response
