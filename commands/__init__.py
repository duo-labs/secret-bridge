from commands.cli import cli

from commands.poll.cli import poll
from commands.webhook.cli import webhook

cli.add_command(poll)
cli.add_command(webhook)
