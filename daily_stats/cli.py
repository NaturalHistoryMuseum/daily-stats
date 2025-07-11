import json
import sys

import click

from daily_stats import __version__
from daily_stats.alma_contents import get_alma_contents
from daily_stats.config import Config
from daily_stats.db import get_engine, models
from daily_stats.dimensions_metrics import get_dimensions_metrics


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


@cli.command()
@click.pass_context
def init_db(ctx):
    """
    Create missing database tables.

    This is for local testing only.
    """
    click.echo(
        'This will create any missing tables. Useful for local testing, but NOT '
        'recommended for production.'
    )
    if click.confirm('Are you sure you want to run this?', default=False):
        click.echo('Creating tables...')
        engine = get_engine(ctx.obj['config'])
        for m in models:
            click.echo(f'Creating {m.__tablename__}')
            m.metadata.create_all(engine)
        click.echo('Done.')
    else:
        click.echo('Cancelled.')


@cli.command()
@click.pass_context
def alma(ctx):
    """
    Get, summarise, and store data from the ExLibris Alma API.
    """
    get_alma_contents(ctx.obj['config'])


@cli.command()
@click.pass_context
def dimensions(ctx):
    """
    Get citations metrics from the dimensions API.
    """
    get_dimensions_metrics(ctx.obj['config'])


if __name__ == '__main__':
    cli(sys.argv[1:])
