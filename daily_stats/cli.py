import click

from daily_stats import __version__


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo(__version__)
