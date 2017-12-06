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
        self.data = {'general': {}, 'reports': {}}
        self.read_config()

    def get_stored_reports(self):
        return self.data.get('reports')

    def update_report(self, name, data):
        if name not in self.data.get('reports').keys():
            self.data.get('reports')[name] = {}
        self.data.get('reports')[name].update(data)

    def save_report(self, name, query, desc=False, variables=False):

        if variables:
            var_dict = {}
            for var in variables:
                key, value = var.split(':')
                var_dict[key] = value
            self.update_report(name, var_dict)

        self.update_report(name, {'query': query})
        if desc:
            self.update_report(name, {'description': desc})

        self.write_config()

    def delete_report(self, delete):
            self.data.get('reports').pop(delete)
            self.write_config()

    def read_config(self):
        self.cfg_file = os.path.join(click.get_app_dir(APP_NAME),
                                     'config.yaml')

        try:
            self.data = yaml.safe_load(open(self.cfg_file))
        except yaml.YAMLError as exc:
            click.echo(exc)
        except EnvironmentError:
            if self.verbose:
                click.echo('Config file not found. Creating one.')
            self.write_config()
        if self.verbose:
            click.echo('Loaded config file %s' % self.cfg_file)

    def write_config(self):

        config_dir = os.path.dirname(self.cfg_file)

        if not os.path.exists(config_dir):
                os.makedirs(config_dir)

        with open(self.cfg_file, 'w') as outfile:
            yaml.safe_dump(self.data, outfile,
                           encoding='utf-8',
                           default_flow_style=False,
                           allow_unicode=True)
        if self.verbose:
            click.echo('Config file updated at %s.' % self.cfg_file)

    def echo_saved_reports(self):
        if not self.get_stored_reports():
            click.secho('No reports saved.', fg='red')
            return
        click.echo('Stored reports:')
        report_name_length = max([len(name) for name in
                                  self.get_stored_reports().keys()])

        for report, cfg in self.get_stored_reports().items():

            if cfg.get('description'):
                click.secho(report.ljust(report_name_length),
                            fg='green', nl=False)
                click.secho(' -- %s' % cfg.get('description'),
                            )
            else:
                click.secho('%s' % report, fg='green')


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(invoke_without_command=True)
@click.option('--ledger', '-l', required=False)
@click.option('--show-config', '-c', required=False)
@click.option('--verbose', is_flag=True)
@pass_config
@click.pass_context
def main(ctx, config, ledger, verbose, show_config):
    """Console script for hreports."""
    if not ctx.invoked_subcommand:
        config.echo_saved_reports()

    if verbose:
        config.verbose = True
        click.echo("Config file %s" % config.cfg_file)

    config.ledger = ledger

    if show_config:
        print(yaml.dump(config.data))


@main.command()
@click.option('--query', '-q', required=False)
@click.option('--save', '-s', required=False)
@click.option('--variables', '-v', required=False, multiple=True)
@click.option('--delete', '-d', required=False)
@click.option('--desc', '-i', required=False)
@pass_config
def create(config, query, save, delete, desc, variables):
    if config.verbose:
        click.echo("Managing report")

    if save and query:
        click.echo('Saving %s report' % save)
        if save in config.get_stored_reports():
            click.confirm('Do you want to overwrite %s?' % save,
                          abort=True)
        config.save_report(save, query, desc, variables)
    elif delete:
        if delete not in config.get_stored_reports():
            raise click.UsageError('Report %s does not exist.' % delete)
        else:
            click.echo('Deleting %s report' % delete)
            config.delete_report(delete)
    elif not delete and not save and query:
        hreport = hreports.Hreport(config)
        click.echo("Running %s" % query)
        click.echo(hreport.run(query=query))
    else:
        config.echo_saved_reports()


@main.command()
@click.argument('name', required=False)
@click.option('--info', '-i', is_flag=True)
@click.option('--template', '-t', required=False)
@click.option('--query', '-q', required=False)
@click.option('--template', '-t', required=False,
              help="Appends additional parameters to report query")
@pass_config
def show(config, name, query, template, info):
    if config.verbose:
        click.echo("Showing reports", nl=True)

    if not name:
        config.echo_saved_reports()
    elif info:
        report_config = config.get_stored_reports().get(name)
        click.echo(yaml.dump(report_config, default_flow_style=False))
    elif name:
        report_config = config.get_stored_reports().get(name)
        if query:
            report_config['query'] += ' %s' % query
        hreport = hreports.Hreport(config, name)
        click.echo(hreport.render(template))


@main.command()
def save():
    click.echo("Saving")


if __name__ == "__main__":
    main()
