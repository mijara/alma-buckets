import dateutil.parser

from datetime import datetime
from datetime import timedelta
from elasticsearch_dsl import Index


def _validate(indexes):
    result = []
    for index in indexes:
        if Index(index).exists():
            result.append(index)
    return result


def get_indexes(prefix, ftime, ttime=None):
    """
    Constructs each index in a time range, using the prefix and appending a
    date format of %Y.%m.%d (eg 2017.02.16), and validates each one of them
    with ElasticSearch, only returning the ones that are valid.

    :param prefix: some prefix before the hyphen
    :param ftime: from time
    :param ttime: to time
    :return: a list of valid ES indexes.
    """
    if ttime is None or ttime == 'now':
        ttime = datetime.utcnow()

    if isinstance(ttime, str):
        ttime = dateutil.parser.parse(ttime)

    if isinstance(ftime, str):
        ftime = dateutil.parser.parse(ftime)

    results = []
    delta = timedelta(days=1)
    pivot = ftime

    while pivot < ttime:
        results.append('%s-%s' % (prefix, pivot.strftime('%Y.%m.%d')))
        pivot += delta

    return _validate(results)
