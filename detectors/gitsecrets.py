import subprocess
import tempfile
import json
import logging

from models.finding import Finding
from detectors.detector import Detector

class GitSecrets(Detector):
    def __init__(self, path=None):
        """Initialize the `git-secrets` wrapper with an optional
        path to the `detect-secrets` binary.
        """
        if path is not None:
            self._binary_path = path
        else:
            self._binary_path = "git-secrets"
        self.logger = logging.getLogger("GitSecrets")

    @property
    def name(self):
        return "git-secrets"

    def run(self, repo_dir, file_obj, commit_link=None):
        """Run `git-secrets` on a repository.

        Arguments:
        repo_dir -- str: the temp directory where this commit is checked out
        file_obj -- a GitHub "file" object from a commit
        see: https://developer.github.com/v3/repos/commits/#get-a-single-commit
        """
        self.logger.info("instantiating git-secrets")
        subprocess.run([self._binary_path, "--register-aws"], cwd=repo_dir, capture_output=True)
        if file_obj is not None:
            sp = subprocess.run([self._binary_path, "--scan", file_obj.filename], cwd=repo_dir, capture_output=True)
        else:
            sp = subprocess.run([self._binary_path, "--scan"], cwd=repo_dir, capture_output=True)

        if sp.returncode not in [0, 1]:
            self.logger.error(sp.stderr.encode())
            raise Exception("Unknown error while running git-secrets. Are bash and GNU grep installed?")

        return self._output_to_findings(sp.stderr, commit_link)

    def _output_to_findings(self, output, commit_link):
        if isinstance(output, bytes):
            output = output.decode()

        findings = []
        for line in output.splitlines():
            # the first non-blank lines of git-secrets output will
            # be findings, so parse those, but ignore empty output
            # and ignore everything after the findings
            if line == '':
                break
            parts = line.split(':')
            findings.append(Finding(parts[0], "generic", parts[2], line_number=parts[1], link=commit_link))
        return findings
