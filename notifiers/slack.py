from notifiers.notifier import Notifier
from notifiers import Registry
from os import getenv
import requests

class SlackWebhookNotifier(Notifier):
    notifier_id = 'slack_webhook'

    def __init__(self, config):
        if config['webhook_url'] == 'env':
            config['webhook_url'] = str(getenv('SLACK_WEBHOOK_URL'))

        if not config['webhook_url']:
            raise Exception("webhook_url not found in config file")

        self._webhook_url = config['webhook_url']

    def process(self, findings, detector_name):
        """Send a list of findings via Slack incoming webhook."""
        requests.post(self._webhook_url, json={"text": "{} found the following:".format(detector_name)})
        for finding in findings:
            requests.post(self._webhook_url, json={"text": str(finding)})


Registry.register(SlackWebhookNotifier.notifier_id, SlackWebhookNotifier)
