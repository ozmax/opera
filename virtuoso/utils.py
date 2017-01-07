from rdflib.plugins.sparql import parser

import requests


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
