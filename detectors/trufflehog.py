import subprocess
import tempfile
import json
import logging

from models.finding import Finding
from detectors.detector import Detector

class TruffleHog(Detector):
    def __init__(self, path=None):
        """Initialize the `trufflehog` wrapper with an optional
        path to the `trufflehog` binary
        """
        if path is not None:
            self._binary_path = path
        else:
            self._binary_path = "trufflehog"
        self.logger = logging.getLogger("TruffleHog")

    @property
    def name(self):
        return "truffleHog"

    def run(self, repo_dir, file_obj, commit_link=None):
        """Run `trufflehog` on a repository.

        Arguments:
        repo_dir -- str: the temp directory where this commit is checked out
        file_obj -- a GitHub "file" object from a commit
        see: https://developer.github.com/v3/repos/commits/#get-a-single-commit
        """
        self.logger.info("instantiating trufflehog")
        #dummy_repo_url value needed by trufflehog as filler field, since no remote repo is being used
        sp = subprocess.run([self._binary_path, "--json", "--repo_path", ".", "dummy_repo_url"], cwd=repo_dir, capture_output=True)

        if sp.returncode not in [0, 1]:
            self.logger.error(sp.stderr.encode())
            raise Exception("Unknown error while running truffleHog.")

        return self._output_json_findings(sp.stdout, commit_link)
    
    def _output_json_findings(self, output, commit_link):
        findings = []
        if isinstance(output, bytes):
            output = output.decode()

        for line in output.splitlines():
            json_line = json.loads(line)

            reason = json_line['reason']
            results = json_line['stringsFound']
            filename = json_line['path']
            findings.append(Finding(filename, reason, str(results), link=commit_link))
        return findings