from models.monitors.monitor import MonitorModel
from models.monitors.pagination import paginate
from state import State

import logging


class User(MonitorModel):
    def __init__(self, username, client):
        self.name = username
        self.event_offset = 0
        stored_offset = State.get('user', self.name)
        if stored_offset:
            self.event_offset = stored_offset
        self.client = client
        self.user = client.get_user(self.name)

    def poll(self):
        events = paginate(self.user.get_events, event_offset=self.event_offset)
        if events:
            logging.info('Found {} events for user {}'.format(
                len(events), self.name))
            self.event_offset = int(events[0].id)
            State.update('user', self.name, self.event_offset)
        return events
