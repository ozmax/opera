from rdflib.plugins.sparql import parser

import requests

from .conf import HEADERS, VIRTUOSO_ENDPOINT


def make_query(data):
    username = data.get('username', '')
    password = data.get('password', '')
    query = data.get('query', '')
    file_query = data.get('upload', '')
    data = query if query else file_query
    headers = HEADERS['sparql_query']

    response = requests.post(
        url=VIRTUOSO_ENDPOINT,
        headers=headers,
        auth=(username, password),
        data=data
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


def send_notif(username, password, target_url, endpoint, resource, predicate):
    data = {
        'username': username,
        'password': password,
        'source': endpoint,
        'resource': resource,
        'predicate': predicate,
    }
    url = '%s/trends/notify/' % target_url
    requests.post(url, data=data)
