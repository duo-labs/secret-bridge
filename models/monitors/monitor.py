from abc import ABC, abstractmethod

class MonitorModel(ABC):
    @abstractmethod
    def poll(self):
        """Polls the appropriate Github Events API for new events associated
        with this model.
        """
        pass