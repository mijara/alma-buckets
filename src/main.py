from search import Searcher
from buckets import OverviewBucket, PrefixBucket, PriorityBucket, FullBucket, \
    PathClassBucket

from args import args
from elasticsearch_dsl.connections import connections
from conf import get_conf


def main():
    # get options from console.
    options = args()

    # get configuration from file.
    config = get_conf(options['config_file'])

    # create ES connection to hosts.
    connections.create_connection(hosts=config['elasticsearch']['hosts'],
                                  timeout=30)

    # create the searcher instance to find alarms, given the options from
    # console.
    searcher = Searcher(options['from'], options['query'],
                        ttime=options['to'], per_page=500,
                        min_priority=options['min_priority'])

    buckets = [
        PathClassBucket(config['kibana'])
    ]

    # manually fetch all alarms from the searcher and pass it to every bucket.
    for alarm in searcher.pages():
        for bucket in buckets:
            bucket.cherry_pick(alarm)

    # dump all buckets, this will print out all buckets.
    for bucket in buckets:
        bucket.dump()


if __name__ == '__main__':
    main()
