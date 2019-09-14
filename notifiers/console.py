from notifiers.notifier import Notifier
from notifiers import Registry

class ConsoleNotifier(Notifier):
    notifier_id = 'console'

    def __init__(self, config):
        super()
        pass

    def process(self, findings, detector_name):
        """Print the findings to the console with a heading for the detector name."""
        print("{} found the following:".format(detector_name))
        for finding in findings:
            print(finding)


Registry.register(ConsoleNotifier.notifier_id, ConsoleNotifier)
