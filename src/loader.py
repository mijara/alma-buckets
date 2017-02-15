import imp
import json
import os

import buckets


def _load_buckets(buckets_conf):
    if 'list' not in buckets_conf:
        return []

    load_libs = [buckets]
    if 'load' in buckets_conf:
        for path in buckets_conf['load']:
            load_libs.append(imp.load_source('custom', path))

    loaded_buckets = []
    for bucket in buckets_conf['list']:
        name = bucket['name']
        arguments = bucket['args']

        for lib in load_libs:
            try:
                bucket = getattr(lib, name)
                loaded_buckets.append(bucket(*arguments))
            except AttributeError:
                continue

    return loaded_buckets


def load_conf():
    conf = {
        'buckets': []
    }

    conf_path = os.path.join(os.path.curdir, 'buckets.json')

    if not os.path.exists(conf_path):
        return conf

    with open(conf_path) as f:
        raw = json.load(f)

        if 'buckets' in raw:
            conf['buckets'] = _load_buckets(raw['buckets'])

    return conf
