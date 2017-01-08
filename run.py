from rdflib.plugins.sparql import parser

queries = {
    'base': 'insert data { <foo> <bar> <baz> ; <bar1> <baz1>}',

    'base_plus':
        """
        PREFIX foo: <http://trilalo.com/>
        insert data {foo:lol1 foo:lol2 foo:lol3}
        """,

    'double_prefixed':
    """
    PREFIX foo: <http://trilalo.com/>
    PREFIX bar: <http://sapiomilo.com/>
    insert data {foo:lol1 foo:lol2 foo:lol3 . foo:qwe1 bar:qwe2 bar:qwe3}


    """,

    'with_prefix':
        """
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <gelaw.net/skata/>
        PREFIX lolwut: <5/>

        INSERT DATA { lolwut:gelaw foaf:foo owl:5 ;  foaf:foo "lala"}
        """,
    'yo':
        """
        PREFIX Sensor: <http://example.com/Equipment.owl#>

        INSERT { ?subject Sensor:test2 ?newValue }

        WHERE {values (?oldValue ?newValue)
                {('testValue1' 'newValue1')
                 ('testValue2' 'newValue2') }
            ?subject Sensor:test1 ?oldValue }
        """,
}

# =============================================================================


def get_value(item, prefix_list):
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


def construct_prefix_list(data):
    prefixes = {}

    for item in data:
        prefix = item.prefix
        iri = item.iri.decode()
        prefixes[prefix] = iri

    return prefixes


p = parser.parseUpdate(queries['with_prefix'])
prefix_list = construct_prefix_list(p['prologue'][0])

all_triplets = []

for triple in p['request'][0]['quads']['triples']:
    triples = []
    for triple_unit in triple:
        value = get_value(triple_unit, prefix_list)
        triples.append(value)
    all_triplets += [triples[i:i + 3] for i in xrange(0, len(triples), 3)]
print all_triplets
