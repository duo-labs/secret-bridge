import unittest
import tempfile

from state import EventState


class TestState(unittest.TestCase):
    def setUp(self):
        self.state_file = tempfile.NamedTemporaryFile(delete=True)
        self.state = EventState()
        self.state.load_file(self.state_file.name)

    def tearDown(self):
        self.state_file.close()

    def test_state_update(self):
        got = self.state.get('organization', 'example')
        self.assertEqual(got, None)

        self.state.update('organization', 'example', 25)
        got = self.state.get('organization', 'example')
        self.assertEqual(got, 25)

    def test_state_flush(self):
        self.state.update('organization', 'example', 25)
        # Load a new state instance to ensure the file was flushed correctly
        new_state = EventState()
        new_state.load_file(self.state_file.name)
        got = new_state.get('organization', 'example')
        self.assertEqual(got, 25)
