from buckets import Bucket


class TestBucket(Bucket):
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
