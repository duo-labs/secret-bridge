from notifiers.notifier import Notifier
from notifiers import Registry
import requests

class SlackWebhookNotifier(Notifier):
    notifier_id = 'slack_webhook'

    def __init__(self, config):
        if config['webhook_url'] is None:
            raise Exception("webhook_url not found in config file")

        self._webhook_url = config['webhook_url']

    def process(self, findings, detector_name):
        """Send a list of findings via Slack incoming webhook."""
        requests.post(self._webhook_url, json={"text": "{} found the following:".format(detector_name)})
        for finding in findings:
            requests.post(self._webhook_url, json={"text": str(finding)})


Registry.register(SlackWebhookNotifier.notifier_id, SlackWebhookNotifier)
