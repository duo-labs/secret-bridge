import toml
import logging

from os import environ

from detectors import AvailableDetectors
from notifiers import Registry
from models.monitors import User, Organization, Repository


class WatcherConfig:
    def __init__(self):
        self._config = {}
        self.access_token = ''
        self.monitors = []
        self.detectors = []
        self.notifiers = []
        self.webhook = {}

    def load_file(self, filepath):
        self._config = toml.load(filepath)

        self.access_token = self._config['auth']['access_token']
        if self.access_token == 'env':
            self.access_token = environ.get('GITHUB_WATCHER_TOKEN')

        self.webhook = self._config['webhook']

        for detector in self._config['detectors']:
            if detector not in AvailableDetectors:
                logging.error(
                    'Unknown detector {} listed in configuration'.format(
                        detector))
                continue
            logging.info('Setting up detector: {}'.format(detector))
            # TODO: Add support for per-detector configuration
            self.detectors.append(AvailableDetectors[detector]())

        for notifier_type, config in self._config['notifiers'].items():
            notifier = Registry.get(notifier_type)
            if not notifier:
                logging.error(
                    'Invalid notifier type: {}'.format(notifier_type))
                continue
            logging.info('Setting up notifier: {}'.format(notifier_type))
            self.notifiers.append(notifier(config))

        self.validate()

    def create_monitors(self, client):
        for organization in self._config['monitors'].get('organizations', []):
            logging.info('Monitoring organization: {}'.format(organization))
            self.monitors.append(Organization(organization, client))
        for user in self._config['monitors'].get('users', []):
            logging.info('Monitoring user: {}'.format(user))
            self.monitors.append(User(user, client))
        for repository in self._config['monitors'].get('repos', []):
            logging.info('Monitoring repository: {}'.format(repository))
            self.monitors.append(Repository(repository, client))

    def validate(self):
        if not self.access_token:
            raise Exception('No access token specified')
        if not self.detectors:
            raise Exception('No detectors provided')


Config = WatcherConfig()
