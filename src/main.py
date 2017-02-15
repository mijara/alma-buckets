from elasticsearch_dsl.connections import connections

from args import args
from loader import load_conf
from search import Searcher
from buckets import OverviewBucket, FullBucket

if __name__ == '__main__':
    options = args()

    connections.create_connection(hosts=['http://isara.osf.alma.cl:9200'], timeout=30)

    searcher = Searcher(options['from'], options['query'],
                        ttime=options['to'], per_page=500)

    print 'Request time range: %s to %s' % (options['from'], options['to'])

    conf = load_conf()

    if conf['buckets'] is not None:
        buckets = conf['buckets']
    else:
        buckets = [
            FullBucket(),
            OverviewBucket(),
            #PrefixBucket('ONLINE'),
            #PriorityBucket('WARNING'),
        ]

    for alarm in searcher.pages():
        for bucket in buckets:
            bucket.cherry_pick(alarm)

    for bucket in buckets:
        bucket.dump()
