import unittest

from models.monitors.mock import MockEvent
from models.monitors.pagination import paginate, PAGE_SIZE
from commands.poll.poller import Poller, DEFAULT_RETRY_COUNT

import requests


class MockPaginator:
    def __init__(self):
        self.offset = 1

    def poll_func(self):
        events = []
        for i in reversed(range(self.offset, self.offset + PAGE_SIZE)):
            events.append(MockEvent(i))
        self.offset = events[0].id
        return events

    def replay_events(self):
        """
        Pretends nothing has happened, returning the "last" PAGE_SIZE
        events
        """
        events = []
        for i in range(self.offset, self.offset - PAGE_SIZE, -1):
            events.append(MockEvent(i))
        return events


class MockRetryMonitor:
    def __init__(self, should_fail=0):
        self.attempts = 0
        self.should_fail = should_fail

    def poll(self):
        self.attempts += 1
        if self.attempts >= self.should_fail:
            return []
        raise requests.exceptions.ConnectionError


class TestPoller(unittest.TestCase):
    def test_pagination(self):
        paginator = MockPaginator()

        # Make sure that paginating without an offset only returns PAGE_SIZE
        # results.
        got = paginate(paginator.poll_func)
        self.assertEqual(len(got), PAGE_SIZE)
        self.assertEqual(got[0].id, paginator.offset)

        # Make sure that paginating with an offset equal to the latest event
        # (e.g. nothing happened) returns 0 results
        last_offset = int(got[0].id)
        got = paginate(paginator.replay_events, event_offset=last_offset)
        self.assertEqual(len(got), 0)

    def test_retries(self):
        """Ensures that the Poller will retry the connection attempt a
        configured number of times, then fail.
        """
        monitor = MockRetryMonitor()
        poller = Poller([monitor])
        got = poller.poll()
        self.assertEqual(monitor.attempts, 1)

        monitor = MockRetryMonitor(should_fail=3)
        poller = Poller([monitor])
        got = poller.poll()
        self.assertEqual(monitor.attempts, 3)

        monitor = MockRetryMonitor(should_fail=10)
        poller = Poller([monitor])
        with self.assertRaises(requests.exceptions.ConnectionError):
            poller.poll()
        self.assertEqual(monitor.attempts, poller.retry_count + 1)


if __name__ == '__main__':
    unittest.main()
