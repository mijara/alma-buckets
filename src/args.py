import argparse
import timeago


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--last', type=str, help="Time to query ES for last logs, overrides from/to")

    parser.add_argument('-f', '--from-time', type=str, help="Time lower limit in UTC")
    parser.add_argument('-t', '--to-time', type=str, help="Time upper limit in UTC")

    opts = parser.parse_args()

    if opts.last is not None:
        from_time = timeago.to_time(opts.last).isoformat()
        to_time = 'now'
    else:
        to_time = opts.to_time if opts.to_time is not None else 'now'
        from_time = opts.from_time

        if from_time is None:
            raise ValueError("One of --from-time or --last must be specified.")

    return {
        'from': from_time,
        'to': to_time,
    }
