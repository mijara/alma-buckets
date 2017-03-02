import json


def get_conf(file_path):
    conf = {
        'elasticsearch': {
            'hosts': ['localhost:9200']
        },
        'kibana': 'localhost:5601'
    }

    if file_path is None:
        return conf

    with open(file_path) as f:
        raw = json.load(f)

        if 'elasticsearch' not in raw:
            raise ValueError('Config file must contain an elasticsearch field')

        if 'hosts' not in raw['elasticsearch']:
            raise ValueError('Config file must contain an elasticsearch.hosts field')

        conf['elasticsearch']['hosts'] = raw['elasticsearch']['hosts']

        if 'kibana' in raw:
            conf['kibana'] = raw['kibana']

    return conf
