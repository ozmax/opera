import requests
from rdflib.plugins.sparql import parser

HEADERS = {
    'sparql_query': {'Content-Type': 'application/sparql-query'},
}

VIRTUOSO_ENDPOINT = 'http://83.212.116.88:8890/DAV/xx/demo'

REGISTERED_ENDPOINTS = [
    'foo'
]


def make_query(data):
    username = data.get('username', '')
    password = data.get('password', '')
    query = data.get('query', '')

    headers = HEADERS['sparql_query']

    response = requests.post(
        url=VIRTUOSO_ENDPOINT,
        headers=headers,
        auth=(username, password),
        data=query
    )
    return response


def get_triplets(query):
    query = query.replace('INSERT', 'INSERT DATA', 1)
    query = query.replace('insert', 'INSERT DATA', 1)
    parsed_query = parser.parseUpdate(query)
    triples = []
    for triple in parsed_query['request'][0]['quads']['triples']:
        proc_triple = (
            triple[0].decode(),
            triple[1].decode(),
            triple[2].decode()
        )
        triples.append(proc_triple)
    return triples


def send_notif(query):
    pass
