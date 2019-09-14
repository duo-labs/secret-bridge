import unittest
from pathlib import Path
from config import Config
from notifiers import Registry
from models.finding import Finding


class TestConsoleNotifier(unittest.TestCase):
    def test_console_notifier(self):
        config_path = Path(__file__).parent.parent / 'config.toml'
        config = Config.load_file(config_path)

        notifier = Registry.get("console")(config)
        findings = [
            Finding("testfile.py", 123, "test_secret_type",
                    "https://www.example.com")
        ]
        notifier.process(findings, 'test-detector')


if __name__ == "__main__":
    unittest.main()
