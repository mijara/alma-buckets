Alma Buckets
============

```
usage: main.py [-h] [-l LAST] [-f FROM_TIME] [-t TO_TIME] [-c CONFIG]
               [-p MIN_PRIORITY]
               query

positional arguments:
  query                 Query string as written in Kibana.

optional arguments:
  -h, --help            show this help message and exit
  -l LAST, --last LAST  Time to query ES for last logs, overrides from/to.
                        Example: 1s, 1m, 2h, 3d, 5w
  -f FROM_TIME, --from-time FROM_TIME
                        Time lower limit in UTC
  -t TO_TIME, --to-time TO_TIME
                        Time upper limit in UTC
  -c CONFIG, --config CONFIG
                        Config file path
  -p MIN_PRIORITY, --min-priority MIN_PRIORITY
                        Minimum priority to fetch.

```
