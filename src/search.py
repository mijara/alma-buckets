import elasticsearch_dsl
import json

from elasticsearch_dsl import Q

import indexes

PRIORITIES = ['INFO', 'WARNING', 'CRITICAL']


def _get_priorities_ignored(min_priority):
    """
    Returns priorities from minimum up.

    >>> _get_priorities_ignored('WARNING')
    ['INFO']

    >>> _get_priorities_ignored('critical')
    ['INFO', 'WARNING']

    >>> _get_priorities_ignored('test') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError:...

    :param min_priority: minimum priority to take.
    :return: a list of priorities.
    """
    min_priority = min_priority.upper()

    if min_priority not in PRIORITIES:
        raise ValueError('Priority minimum must be one of: ' + ' '.join(PRIORITIES))

    index = PRIORITIES.index(min_priority)
    return PRIORITIES[:index]


class Alarm(object):
    def __init__(self, hit):
        self.name = hit['name'] if 'name' in hit else 'UNNAMED'
        self.timestamp = hit['@timestamp']
        self.priority = hit['priority'] if 'priority' in hit else 'INVALID'
        self.body = hit['body'].to_dict() if 'body' in hit else {}

    def __str__(self):
        return "%s %s %s :: %s" % (self.timestamp, self.priority, self.name,
                                   json.dumps(self.body))


class Searcher(object):
    def __init__(self, ftime, query, ttime=None, per_page=250,
                 min_priority=None):
        """
        Creates a new alarm searcher object, given a from time and optional to
        time. Results can be asked all at once or paginated, every result is
        returned as an alarm object.

        :param ftime: from time in UTC.
        :param ttime: to time in UTC, can be omitted.
        :param per_page: results per page for pagination.
        """
        self.ftime = ftime
        self.ttime = ttime
        self.per_page = per_page
        self.query = query

        inds = indexes.get_indexes('alarm', ftime, ttime)

        # create the search object.
        self.search = elasticsearch_dsl.Search(index=inds)

        # sort by timestamp ascending.
        self.search = self.search.sort({
            "@timestamp": {
                "order": "asc",
                "unmapped_type": "boolean"
            }
        })

        # specify the time range.
        self.search = self.search.filter({
            'range': {
                '@timestamp': {
                    'gte': self.ftime,
                    'lte': 'now',
                }
            }
        })

        if min_priority is not None:
            for p in _get_priorities_ignored(min_priority):
                self.search = self.search.query(~Q("match", priority=p))

        # use query.
        self.search = self.search.query("query_string", query=self.query,
                                        analyze_wildcard=True)

    def get_all(self):
        """
        Returns all results as a generator object.
        :return: a generator of results.
        """
        response = self.search[:self.search.count()]

        # for every hit, create an alarm object and yield it.
        for hit in response:
            yield Alarm(hit)

    def page(self, num):
        """
        Returns each result of one page as a generator.

        :param num: number of the page, starting with 0.
        :return: a generator object of each result.
        """
        start = num * self.per_page
        end = (num + 1) * self.per_page

        response = self.search[start:end].execute()

        for hit in response:
            yield Alarm(hit)

    def pages(self):
        """
        Much like get_all but using pages, in order to avoid large data
        transfer all at once.

        :return: a generator for each result.
        """
        current_page = 0

        while True:
            alarms = []
            for alarm in self.page(current_page):
                alarms.append(alarm)

            if len(alarms) == 0:
                return
            else:
                for alarm in alarms:
                    yield alarm

            current_page += 1
