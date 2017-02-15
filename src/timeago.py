from datetime import datetime, timedelta


SECONDS_PER_UNIT = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
}


def to_time(s, now=None):
    try:
        number = int(s[:-1])
    except ValueError:
        raise SyntaxError('not an integer number: %s' % s[:-1])

    unit = s[-1]
    if unit not in SECONDS_PER_UNIT:
        raise SyntaxError('not a valid time unit: %s, must be one of s, m, h, d, w' % unit)

    if now is None:
        now = datetime.utcnow()
    else:
        if not isinstance(now, datetime):
            raise ValueError('`now` argument must be a datetime')

    return now - timedelta(seconds=number * SECONDS_PER_UNIT[unit])


if __name__ == '__main__':
    now = datetime.utcnow()
    print 'Time now is: %s' % now
    print '1h ago:      %s' % to_time('1h', now=now)
