from rdflib.plugins.sparql import parser


def _get_value(item, prefix_list):
    value = ''
    class_name = item.__class__.__name__

    if class_name == 'URIRef':
        value = item.decode()
    elif class_name == 'CompValue':
        values = item.values()
        if len(values) == 2:
            prefix = values[0]
            iri = values[1]
            value = prefix_list[prefix] + iri
        else:
            value = item.values()[0].decode()
    elif class_name == 'Literal':
        value = item.decode()

    return value


def _construct_prefix_list(data):
    prefixes = {}

    for item in data:
        prefix = item.prefix
        iri = item.iri.decode()
        prefixes[prefix] = iri

    return prefixes


def parse_query(query):

    query = query.replace('INSERT', 'INSERT DATA', 1)
    query = query.replace('insert', 'INSERT DATA', 1)

    parsed = parser.parseUpdate(query)
    prefix_list = _construct_prefix_list(parsed['prologue'][0])

    parsed_triplets = []

    for triple_set in parsed['request'][0]['quads']['triples']:
        triples = []
        for triple_unit in triple_set:
            value = _get_value(triple_unit, prefix_list)
            triples.append(value)
        parsed_triplets += [
            triples[i:i + 3] for i in xrange(0, len(triples), 3)
        ]

    return parsed_triplets
