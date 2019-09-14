from abc import ABC, abstractmethod

class Notifier(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, findings, detector_name):
        """Process a found secret."""
        pass
