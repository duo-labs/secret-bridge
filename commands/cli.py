import click
import sys
import logging

from github import Github
from os import environ

from config import Config
from processor import Processor
from state import State


@click.group()
@click.pass_context
@click.option('-f',
              '--config',
              'config_filename',
              default='config.toml',
              required=False,
              type=click.Path(exists=True),
              show_default=True)
@click.option('-v',
              '--verbose',
              is_flag=True,
              default=False,
              help='Print verbose debug information')
def cli(ctx, config_filename, verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    ctx.obj = {}
    # Load the config, saving the result in the context. If there's an error,
    # chances are it'll panic here.
    try:
        Config.load_file(config_filename)
    except Exception as e:
        click.secho(str(e), fg='red')
        sys.exit(1)

    # Create the global Github API client and store it in the context
    client = Github(Config.access_token)
    ctx.obj['client'] = client

    Processor.configure_client(client)
    Processor.configure_detectors(Config.detectors)
    Processor.configure_notifiers(Config.notifiers)

    State.load_file()
