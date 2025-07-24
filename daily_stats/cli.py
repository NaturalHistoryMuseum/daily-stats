import json
import sys

import click
import sqlalchemy as sa

from daily_stats import __version__
from daily_stats.config import Config
from daily_stats.db import get_engine, get_sessionmaker, models
from daily_stats.stats import (
    get_alma_contents,
    get_dimensions_metrics,
    get_gbif_citations,
    get_package_comp,
    get_portal_images,
)


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
def test_conn(ctx):
    """
    Test the connection to the database by selecting the first row of each table.
    """
    click.echo(f'Connecting to {ctx.obj["config"].db_url}...')

    sessionmaker = get_sessionmaker(ctx.obj['config'])
    with sessionmaker.begin() as session:
        for m in models:
            click.echo(f'Selecting a row from {m.__tablename__}:')
            select_stmt = sa.select(m).limit(1)
            row = session.scalars(select_stmt).first()
            click.echo(row)
            click.echo()


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


@cli.command()
@click.pass_context
def gbif_citations(ctx):
    """
    Get citation data from GBIF.
    """
    get_gbif_citations(ctx.obj['config'])


@cli.command()
@click.pass_context
def package_comp(ctx):
    """
    Get dataset statistics from the NHM data portal.
    """
    get_package_comp(ctx.obj['config'])


@cli.command()
@click.pass_context
def portal_images(ctx):
    """
    Get specimen image statistics from the NHM data portal.
    """
    get_portal_images(ctx.obj['config'])


if __name__ == '__main__':
    cli(sys.argv[1:])
