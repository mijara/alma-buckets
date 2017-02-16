Alma Buckets
============

ElasticSearch alarm formatter for Jenkins Email Templates.

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

## Why Buckets?

This software uses the concept of Buckets to store information about alarms. 
Each bucket receives each alarm and determines if it is useful for it's 
operation or not, afterwards the bucket should display information collected to
the output. This output will effectively be used by Jenkins to send an email.

For example the OverviewBucket will collect how many of each type of alarm
priority there're, and print something like:

    INFO: 17
    WARNING: 42
    CRITICAL: 31

Bundled with this software there's also the PriorityBucket, PrefixBucket and
FullBucket. Check the docts of the buckets module for a description of each 
one.
