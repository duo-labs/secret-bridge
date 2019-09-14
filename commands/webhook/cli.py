import click
import logging

from config import Config
from commands.webhook.server import app


@click.command(name='webhook')
@click.pass_context
def webhook(ctx):
    secret = Config.webhook.get('secret')
    if not secret:
        logging.error('No webhook secret configured.')
        return
    app.config['GITHUB_WEBHOOK_SECRET'] = secret
    logging.info('Starting webhook server at /webhook')
    app.run(host=Config.webhook.get('host', '0.0.0.0'))
