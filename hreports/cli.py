# -*- coding: utf-8 -*-

"""Console script for hreports."""

import click
import os

APP_NAME = 'hreports'


class Config(object):

    def __init__(self):
        self.verbose = False
        self.read_config()

    def read_config(self):
        self.cfg = os.path.join(click.get_app_dir(APP_NAME), 'config.yaml')


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(invoke_without_command=True)
@click.option('--verbose', is_flag=True)
@pass_config
@click.pass_context
def main(ctx, config, verbose):
    """Console script for hreports."""
    if not ctx.invoked_subcommand:
        click.echo("Show reports")

    if verbose:
        config.verbose = True
        click.echo("Config file %s" % config.cfg)


@main.command()
@pass_config
def create(config):
    if config.verbose:
        click.echo("Create a report")


@main.command()
def show():
    click.echo("Show")


@main.command()
def save():
    click.echo("Saving")


if __name__ == "__main__":
    main()
