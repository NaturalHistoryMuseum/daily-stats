import json
import sys

import click

from daily_stats import __version__
from daily_stats.config import Config


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, default=False)
@click.pass_context
def cli(ctx, version):
    """
    Basic CLI for easily running daily stats scripts.
    """
    if version or ctx.invoked_subcommand is None:
        click.echo(__version__)
        sys.exit(0)
    config = Config()
    ctx.obj = {'config': config}


@cli.command()
@click.pass_context
def get_config(ctx):
    """
    Print the current configuration.
    """
    click.echo(json.dumps(ctx.obj['config'].as_dict(), indent=2))
