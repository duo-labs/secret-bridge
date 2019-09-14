import unittest
from unittest.mock import patch
from pathlib import Path
from os import environ
from config import Config
from notifiers import Registry
from notifiers.slack import SlackWebhookNotifier
from models.finding import Finding


class TestSlackIntegration(unittest.TestCase):
    @patch('requests.post')
    def test_webhook_url(self, mock_post):
        environ['GITHUB_WATCHER_TOKEN'] = 'abcdef'
        # sorta hacky -- we get more than one notifier loaded with the default
        # config and we can't get it by name, so loop through all of them
        notifier = None
        for n in Config.notifiers:
            if isinstance(n, SlackWebhookNotifier):
                notifier = n
                break
        findings = [
            Finding("testfile.py", 123, "test_secret_type",
                    "https://www.example.com")
        ]
        notifier.process(findings, 'test-detector')


if __name__ == "__main__":
    unittest.main()
