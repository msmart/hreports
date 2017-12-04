# -*- coding: utf-8 -*-

"""Console script for hreports."""

import click
import os
import yaml

import hreports

APP_NAME = 'hreports'


class Config(object):

    def __init__(self):
        self.verbose = False
        self.reports = {}
        self.read_config()

    def read_config(self):
        self.cfg_file = os.path.join(click.get_app_dir(APP_NAME),
                                     'config.yaml')

        try:
            self.__dict__ = yaml.safe_load(open(self.cfg_file))
        except yaml.YAMLError as exc:
            click.echo(exc)
        except EnvironmentError:
            if self.verbose:
                click.echo('Config file not found. Creating one.')
            self.write_config(self.__dict__)
        if self.verbose:
            click.echo('Loaded config file %s' % self.cfg_file)

    def write_config(self, config=None):
        if not config:
            config = self.__dict__
        config_dir = os.path.dirname(self.cfg_file)

        if not os.path.exists(config_dir):
                os.makedirs(config_dir)

        with open(self.cfg_file, 'w') as outfile:
            yaml.safe_dump(config, outfile,
                           encoding='utf-8',
                           default_flow_style=False,
                           allow_unicode=True)
        if self.verbose:
            click.echo('Config file updated at %s.' % self.cfg_file)


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
        click.echo("Config file %s" % config.cfg_file)


@main.command()
@click.option('--query', '-q', required=False)
@click.option('--save', '-s', required=False)
@click.option('--delete', '-d', required=False)
@pass_config
def create(config, query, save, delete):
    if config.verbose:
        click.echo("Managing report")

    if save:
        click.echo('Saving %s report' % save)
        hreport = hreports.Create(save, query)
        if save in config.reports:
            click.confirm('Do you want to overwrite %s?' % save,
                          abort=True)
        config.reports.update({save: hreport.__dict__})
        config.write_config()
    elif delete:
        if delete not in config.reports:
            raise click.UsageError('Report %s does not exist.' % delete)
        else:
            click.echo('Deleting %s report' % delete)
            config.reports.pop(delete)
            config.write_config()
    else:
        hreport = hreports.Create(None, query)
        click.echo("Running %s" % hreport.query)
        click.echo(hreport.run())


@main.command()
@click.argument('name', required=False)
@pass_config
def show(config, name):
    if config.verbose:
        click.echo("Show reports", nl=True)

    if not name:
        if not config.reports.keys():
            click.secho('No reports saved.', fg='red')
        for report in config.reports.keys():
            click.secho('%s' % report, fg='green')


@main.command()
def save():
    click.echo("Saving")


if __name__ == "__main__":
    main()
