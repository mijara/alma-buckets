import json
from buckets import OverviewBucket, PrefixBucket, PriorityBucket, FullBucket


def _convert_buckets(buckets):
    result = []

    for bucket in buckets:
        try:
            if bucket['name'] == 'overview':
                result.append(OverviewBucket())
            elif bucket['name'] == 'priority':
                value = bucket['value']
                result.append(PriorityBucket(value))
            elif bucket['name'] == 'prefix':
                value = bucket['value']
                result.append(PrefixBucket(value))
            elif bucket['name'] == 'full':
                result.append(FullBucket())
            else:
                raise ValueError('invalid bucket definition: ' + str(bucket))

        except KeyError:
            raise ValueError('invalid bucket definition: ' + str(bucket))

    return result


def get_conf(file_path):
    conf = {
        'elasticsearch': {
            'hosts': ['localhost:9200']
        },
        'buckets': [
            {
                'name': 'overview'
            }
        ]
    }

    if file_path is None:
        return conf

    with open(file_path) as f:
        raw = json.load(f)

        if 'elasticsearch' not in raw:
            raise ValueError('config file must contain an elasticsearch field')

        if 'hosts' not in raw['elasticsearch']:
            raise ValueError(
                'config file must contain an elasticsearch.hosts field')

        conf['elasticsearch']['hosts'] = raw['elasticsearch']['hosts']

        if 'buckets' in raw:
            conf['buckets'] = raw['buckets']

        conf['buckets'] = _convert_buckets(conf['buckets'])

    return conf
