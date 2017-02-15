class Bucket(object):
    GUARD_FORMAT = "==== {0} ===="

    def cherry_pick(self, alarm):
        raise NotImplementedError()

    def dump_content(self):
        raise NotImplementedError()

    def get_guard(self):
        raise NotImplementedError()

    def dump(self):
        if not self.has_content():
            return

        guard = self.get_guard()

        print self.GUARD_FORMAT.format("BEGIN " + guard)
        self.dump_content()
        print self.GUARD_FORMAT.format("END " + guard)

    def has_content(self):
        raise NotImplementedError()


class FullBucket(Bucket):
    def __init__(self):
        self.picked = []

    def get_guard(self):
        return "FULL"

    def cherry_pick(self, alarm):
        self.picked.append(str(alarm))

    def has_content(self):
        return len(self.picked) > 0

    def dump_content(self):
        for alarm in self.picked:
            print alarm


class OverviewBucket(Bucket):
    def __init__(self):
        self.counters = {
            'INFO': 0,
            'WARNING': 0,
            'CRITICAL': 0,
        }

    def cherry_pick(self, alarm):
        if alarm.priority not in self.counters:
            self.counters[alarm.priority] = 0
        self.counters[alarm.priority] += 1

    def dump_content(self):
        print 'CRITICAL = %d' % self.counters['CRITICAL']
        print 'WARNING  = %d' % self.counters['WARNING']
        print 'INFO     = %d' % self.counters['INFO']

    def get_guard(self):
        return "OVERVIEW"

    def has_content(self):
        return True


class PrefixBucket(Bucket):
    def __init__(self, prefix):
        self.prefix = prefix
        self.picked = []

    def get_guard(self):
        return 'PREFIX "%s"' % self.prefix

    def cherry_pick(self, alarm):
        if alarm.name.startswith(self.prefix):
            self.picked.append(str(alarm))

    def dump_content(self):
        for alarm in self.picked:
            print alarm

    def has_content(self):
        return len(self.picked) > 0


class PriorityBucket(Bucket):
    def __init__(self, priority):
        self.priority = priority
        self.picked = []

    def get_guard(self):
        return 'PRIORITY "%s"' % self.priority

    def cherry_pick(self, alarm):
        if alarm.priority == self.priority:
            self.picked.append(str(alarm))

    def dump_content(self):
        for alarm in self.picked:
            print alarm

    def has_content(self):
        return len(self.picked) > 0
