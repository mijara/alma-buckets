import elasticsearch_dsl
import json

import indexes

PRIORITIES = ['INFO', 'WARNING', 'CRITICAL']


class Alarm(object):
    def __init__(self, hit):
        self.name = hit['name'] if 'name' in hit else 'UNNAMED'
        self.timestamp = hit['@timestamp'] if '@timestamp' in hit else 'INVALID'
        self.priority = hit['priority'] if 'priority' in hit else 'INVALID'
        self.body = hit['body'].to_dict() if 'body' in hit else {}

    def __str__(self):
        return "%s %s %s :: %s" % (self.timestamp, self.priority, self.name, json.dumps(self.body))


class Searcher(object):
    def __init__(self, ftime, query, ttime=None, per_page=250):
        """
        Creates a new alarm searcher object, given a from time and optional to time.
        Results can be asked all at once or paginated, every result is returned as
        an alarm object.

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

        # use query.
        self.search = self.search.query("query_string", query=self.query, analyze_wildcard=True)

    def get_all(self):
        response = self.search[:self.search.count()]

        # for every hit, create an alarm object and yield it.
        for hit in response:
            yield Alarm(hit)

    def page(self, num):
        start = num * self.per_page
        end = (num + 1) * self.per_page

        response = self.search[start:end].execute()

        for hit in response:
            yield Alarm(hit)

    def pages(self):
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
