import click
import logging
import time

from config import Config
from commands.poll.poller import Poller


@click.command(name='poll')
@click.pass_context
def poll(ctx):
    client = ctx.obj['client']
    Config.create_monitors(client)
    poller = Poller(Config.monitors)
    while True:
        try:
            poller.poll()
            logging.info('Sleeping')
            time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Interrupt received... Exiting")
            break
