from detectors.detectsecrets import DetectSecrets
from detectors.gitsecrets import GitSecrets
from detectors.trufflehog import TruffleHog
# TODO: Turn this into a registry to match the notifiers pattern?
AvailableDetectors = {
    'detect-secrets': DetectSecrets,
    'git-secrets': GitSecrets,
    'trufflehog': TruffleHog
}
