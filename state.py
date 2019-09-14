import os
import logging
import json


class EventState:
    def __init__(self):
        self.state = {
            'monitors': {
                'organization': {},
                'user': {},
                'repository': {}
            }
        }
        self.state_filename = ''

    def load_file(self, filename='state.json'):
        self.state_filename = filename
        if os.path.exists(filename):
            with open(filename, 'r') as state_file:
                try:
                    self.state = json.loads(state_file.read())
                    return
                except Exception as e:
                    logging.info(
                        'Error loading existing state information from {}. Creating a new state file'
                        .format(filename))
        else:
            logging.info('No state file found, creating a new one')
        self.flush()

    def update(self, type, key, value):
        self.state['monitors'][type][key] = value
        self.flush()

    def get(self, type, key):
        if type not in self.state['monitors']:
            return None
        if key not in self.state['monitors'][type]:
            return None
        return self.state['monitors'][type][key]

    def flush(self):
        logging.debug('Flusing state file to {}'.format(self.state_filename))
        with open(self.state_filename, 'w') as state_file:
            state_file.write(json.dumps(self.state))


State = EventState()
