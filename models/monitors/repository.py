from models.monitors.monitor import MonitorModel
from models.monitors.pagination import paginate
from state import State

import logging


class Repository(MonitorModel):
    def __init__(self, repository_name, client):
        self.name = repository_name
        self.event_offset = 0
        stored_offset = State.get('repository', self.name)
        if stored_offset:
            self.event_offset = stored_offset
        self.client = client
        self.repo = client.get_repo(self.name)

    def poll(self):
        events = paginate(self.repo.get_events, event_offset=self.event_offset)
        if events:
            logging.info('Found {} events for repository {}'.format(
                len(events), self.name))
            self.event_offset = int(events[0].id)
            State.update('repository', self.name, self.event_offset)
        return events
