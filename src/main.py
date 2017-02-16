from search import Searcher
from buckets import OverviewBucket, PrefixBucket, PriorityBucket, FullBucket

from args import args
from elasticsearch_dsl.connections import connections
from conf import get_conf


def main():
    options = args()
    config = get_conf(options['config_file'])

    connections.create_connection(hosts=config['elasticsearch']['hosts'], timeout=30)

    searcher = Searcher(options['from'], options['query'],
                        ttime=options['to'], per_page=500,
                        min_priority=options['min_priority'])

    print 'Request time range: %s to %s' % (options['from'], options['to'])

    buckets = [
        OverviewBucket(),
        PrefixBucket('ONLINE'),
        PrefixBucket('OFFLINE'),
    ]

    for alarm in searcher.pages():
        for bucket in buckets:
            bucket.cherry_pick(alarm)

    for bucket in buckets:
        bucket.dump()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print e
