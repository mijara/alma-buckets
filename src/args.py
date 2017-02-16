import argparse
import timeago


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--last', type=str,
                        help='Time to query ES for last logs, overrides '
                             'from/to. Example: 1s, 1m, 2h, 3d, 5w')

    parser.add_argument('-f', '--from-time', type=str,
                        help='Time lower limit in UTC')

    parser.add_argument('-t', '--to-time', type=str,
                        help='Time upper limit in UTC')

    parser.add_argument('-c', '--config', type=str,
                        help='Config file path')

    parser.add_argument('-p', '--min-priority', default='INFO', type=str,
                        help='Minimum priority to fetch.')

    parser.add_argument('query', type=str,
                        help='Query string as written in Kibana.')

    opts = parser.parse_args()

    if opts.last is not None:
        from_time = timeago.to_time(opts.last).isoformat()
        to_time = 'now'
    else:
        to_time = opts.to_time if opts.to_time is not None else 'now'
        from_time = opts.from_time

        if from_time is None:
            raise ValueError('One of --from-time or --last must be specified.')

    return {
        'from': from_time,
        'to': to_time,
        'query': opts.query,
        'config_file': opts.config,
        'min_priority': opts.min_priority,
    }
