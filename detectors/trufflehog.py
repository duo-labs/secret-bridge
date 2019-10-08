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
        sp = subprocess.run([self._binary_path, "--repo_path", ".", "dummy_repo_url"], cwd=repo_dir, capture_output=True)

        if sp.returncode not in [0, 1]:
            self.logger.error(sp.stderr.encode())
            raise Exception("Unknown error while running truffleHog.")

        return self._output_to_findings(sp.stdout, commit_link)

    def _output_to_findings(self, output, commit_link):
        if isinstance(output, bytes):
            output = output.decode()

        Reason = ''
        Hash = ''
        Filepath = ''
        Branch = ''
        Commit = ''

        findings = []

        for line in output.splitlines():
            # trufflehog output is split across lines with
            # *nix specific characters. cleaning cleaning
            # and multi-line parsing needed to get clean fields
            # across all result sets that are introduced as a
            # single blob

            parts = line.split(':')
            if "Reason" in parts[0]:
                Reason = parts[1].replace('\x1b[92m','').replace('\x1b[0m','')
            if "Hash" in parts[0]:
                Hash = parts[1].replace('\x1b[92m','').replace('\x1b[0m','')
            if "Filepath" in parts[0]:
                Filepath = parts[1].replace('\x1b[92m','').replace('\x1b[0m','')
            if "Branch" in parts[0]:
                Branch = parts[1].replace('\x1b[92m','').replace('\x1b[0m','')
            if "Commit" in parts[0]:
                Commit = parts[1].replace('\x1b[92m','').replace('\x1b[0m','')
            if Commit is not '':
                findings.append(Finding(Filepath, Reason, "unknown",None,commit_link+"/commit/"+Hash.strip()))
                Reason = ''
                Hash = ''
                Filepath = ''
                Branch = ''
                Commit = ''
        return findings
