# -*- coding: utf-8 -*-

"""Console script for hreports."""

import click



@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """Console script for hreports."""
    if not ctx.invoked_subcommand:
        click.echo("Show reports")


@main.command()
def create():
    click.echo("Create")


@main.command()
def show():
    click.echo("Show")


@main.command()
def save():
    click.echo("Saving")


if __name__ == "__main__":
    main()
