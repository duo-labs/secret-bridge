from abc import ABC, abstractmethod

class Detector(ABC):
    """Detector is the abstract class that all detector implementations
    must inherit from.
    """

    @property
    @abstractmethod
    def name(self):
        """A constant string representing the name of the detector.
        Ex: "git-secrets", "detect-secrets"
        """
        pass

    @abstractmethod
    def __init__(self, path=None):
        """Arguments:
        path: str -- the path to the detector binary if outside of PATH
        """
        pass

    @abstractmethod
    def run(self, repo_dir, file_obj):
        """Run the detector and return a list of findings.

        Arguments:
        repo_dir: str -- the path to the cloned repository
        """
        pass
