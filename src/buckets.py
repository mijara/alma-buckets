class Bucket(object):
    """
    A Bucket is an object that collects alarms, and potentially
    displays useful information to STDOUT for Jenkins to parse.

    For each alarm that the searcher collects, this object
    cherry_pick method gets called with that alarm.
    """

    # Guard format for bars.
    GUARD_FORMAT = "==== {0} ===="

    def cherry_pick(self, alarm):
        """
        the Cherry Pick method receives an alarm to analyze it,
        the intention is that the bucket decides if the alarm is
        useful or not.

        :param alarm: the Alarm object
        """
        raise NotImplementedError()

    def dump_content(self):
        """
        Must dump the content of this Bucket to STDOUT (print it).
        """
        raise NotImplementedError()

    def get_guard(self):
        """
        Returns the guard bars for Jenkins to identify. For
        example the OverviewBucket returns "OVERVIEW".

        :return: a guard string
        """
        raise NotImplementedError()

    def has_content(self):
        """
        Returns True if this Bucket has any content to display.

        :return: a bool
        """
        raise NotImplementedError()

    def dump(self):
        """
        Dumps the guards and content to STDOUT. Omits
        the process if the bucket has no content.
        """
        # omit output if there's no content.
        if not self.has_content():
            return

        guard = self.get_guard()

        print self.GUARD_FORMAT.format("BEGIN " + guard)
        self.dump_content()
        print self.GUARD_FORMAT.format("END " + guard)


class FullBucket(Bucket):
    """
    The Full Bucket will display each alarm.
    """
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
    """
    The Overview Bucket will sum each type of alarm
    by priority and display each type along with it's
    sum.

    Example:
    CRITICAL: 42
    WARNING: 137
    INFO: 290
    """
    def __init__(self):
        self.counters = {}

    def cherry_pick(self, alarm):
        if alarm.priority not in self.counters:
            self.counters[alarm.priority] = 0
        self.counters[alarm.priority] += 1

    def dump_content(self):
        for key, value in self.counters.items():
            print "%s: %d" % (key, value)

    def get_guard(self):
        return "OVERVIEW"

    def has_content(self):
        sum = 0
        for value in self.counters.values():
            sum += value
        return sum > 0


class PrefixBucket(Bucket):
    """
    The Prefix Bucket will collect alarms whose name begin
    with some prefix, and then it will display all of them.
    """
    def __init__(self, prefix):
        self.prefix = prefix
        self.picked = []

    def get_guard(self):
        return 'PREFIX "%s"' % self.prefix

    def cherry_pick(self, alarm):
        if alarm.path.startswith(self.prefix):
            self.picked.append(str(alarm))

    def dump_content(self):
        for alarm in self.picked:
            print alarm

    def has_content(self):
        return len(self.picked) > 0


class PriorityBucket(Bucket):
    """
    The Priority Bucket will collect all alarm that have
    a certain priority and display all of them.
    """
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
