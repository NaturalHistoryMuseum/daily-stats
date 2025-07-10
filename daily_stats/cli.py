import json

import click

from daily_stats import __version__
from daily_stats.config import Config


@click.group()
@click.pass_context
def cli(ctx):
    config = Config()
    ctx.obj = {'config': config}


@cli.command()
def version():
    click.echo(__version__)


@cli.command()
@click.pass_context
def get_config(ctx):
    click.echo(json.dumps(ctx.obj['config'].as_dict(), indent=2))
