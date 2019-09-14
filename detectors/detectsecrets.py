import subprocess
import tempfile
import json
import logging

from models.finding import Finding
from detectors.detector import Detector

class DetectSecrets(Detector):
    def __init__(self, path=None):
        """Initialize the `detect-secrets` wrapper with an optional
        path to the `detect-secrets` binary.
        """
        if path is not None:
            self._binary_path = path
        else:
            self._binary_path = "detect-secrets"
        self.logger = logging.getLogger("DetectSecrets")

    @property
    def name(self):
        return "detect-secrets"

    def run(self, repo_dir, file_obj, commit_link=None):
        """Run `detect-secrets` on the contents of a commit.
        We're not using the temporary cloned repo because we want to scan
        patch contents, not files in the repo.

        Arguments:
        repo_dir -- str: the temp directory where this commit is checked out
        file_obj -- a GitHub "file" object from a commit
        see: https://developer.github.com/v3/repos/commits/#get-a-single-commit
        """
        # short-circuit if we don't get a file_obj, like when we're doing
        # baseline scanning
        if file_obj is None:
            return []

        self.logger.info("instantiating detect-secrets on patch contents modifying {}".format(file_obj.filename))
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(file_obj.patch.encode())
            tmp.flush()
            sp = subprocess.run([self._binary_path, "scan", tmp.name], capture_output=True)
            try:
                ds_output = json.loads(sp.stdout)
            except:
                raise Exception("couldn't parse detect-secrets output!")

            return self._json_to_findings(ds_output, file_obj.filename, commit_link)

    def _json_to_findings(self, parsed_output, filename, commit_link):
        results = parsed_output["results"]
        findings = []
        for _, file_results in results.items():
            for file_result in file_results:
                findings.append(Finding(filename, file_result["type"], file_result["hashed_secret"], link=commit_link))
        return findings
