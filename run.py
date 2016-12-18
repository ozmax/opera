import requests

url = 'http://localhost:8000/trends/notify/'

data = {
    'username': 'admin',
    'password': 'pass',

    'source': 'foo',
    'resource': 'http://bar.com/baz/',
    'predicate': 'sameAs',
}

r = requests.post(url, data)
print r
