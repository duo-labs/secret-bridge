from notifiers.registry import NotifierRegistry

Registry = NotifierRegistry()

# import notifiers here, which will auto-register
from .slack import SlackWebhookNotifier
from .console import ConsoleNotifier
