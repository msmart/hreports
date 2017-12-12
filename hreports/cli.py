# -*- coding: utf-8 -*-

"""Console script for hreports."""

import os
import click
import yaml

import hreports
from .config import Config


@click.group(invoke_without_command=True)
@click.option('--ledger', '-l', required=False)
@click.option('--query', '-q', required=False)
@click.option('--config-file', '-c', is_flag=True)
@click.option('--verbose', is_flag=True)
@click.option('--report-config', '-r', required=False)
@click.version_option()
@click.pass_context
def main(context, config_file, ledger, verbose, query, report_config):
    """Console script for hreports."""
    config = Config()
    context.obj = config
    context.obj.ledger = ledger

    if verbose:
        config.verbose = True
        click.echo("Config file %s" % config.cfg_file)
    if not context.invoked_subcommand and query:
        hreport = hreports.Hreport(config)
        click.echo("Running %s" % query)
        click.echo(hreport.run_query(query))
    elif report_config:
        report_config = config.get_stored_reports().get(report_config)
        click.echo(yaml.dump(report_config, default_flow_style=False))
    elif config_file:
        print(yaml.dump(config.data))
    elif not context.invoked_subcommand:
        config.echo_saved_reports()


@main.command()
@click.argument('name')
@click.option('--query', '-q', required=False)
@click.option('--template', '-t', required=False)
@click.option('--desc', '-d', required=False)
@click.option('--variables', '-var', required=False,
              type=(str, str), multiple=True)
@click.pass_obj
def create(config, name, variables, **meta):
    click.echo('Saving %s report' % name)
    if name in config.get_stored_reports():
        click.confirm('Do you want to overwrite %s?' % name,
                      abort=True)
        config.delete_report(name)
    config.update_report(name, meta, variables)


@main.command()
@click.argument('name')
@click.option('--query', '-q', required=False)
@click.option('--template', '-t', required=False)
@click.option('--filename', '-f', required=False)
@click.option('--desc', '-d', required=False)
@click.option('--ledger', '-l', required=False)
@click.option('--variables', '-var', required=False,
              type=(str, str), multiple=True)
@click.pass_obj
def update(config, name, variables, **meta):
    click.echo('Updating  %s report' % name)
    config.update_report(name, meta, variables)


@main.command()
@click.argument('name')
@click.pass_obj
def delete(config, name):
    if name not in config.get_stored_reports():
        raise click.UsageError('Report %s does not exist.' % name)
    else:
        click.echo('Deleting %s report' % name)
        config.delete_report(name)


@main.command()
@click.argument('name', required=False)
@click.option('--template', '-t', required=False)
@click.option('--filename', '-f', required=False)
@click.option('--query', '-q', required=False,
              help="Appends additional parameters to report query")
@click.pass_obj
def show(config, name, query, template, **kwargs):

    if config.verbose:
        click.echo("Showing reports", nl=True)

    if not name:
        config.echo_saved_reports()
    elif name:
        report_config = config.get_stored_reports().get(name)
        if query:
            report_config['query'] += ' %s' % query
        hreport = hreports.Hreport(config)
        click.echo(hreport.render(name, template))


@main.command()
@click.argument('source')
@click.argument('target')
@click.pass_obj
def copy(config, source, target):
    source_config = config.get_stored_reports().get(source, None)

    if not source_config:
        raise click.UsageError('Report %s does not exist.' % source)

    if target in config.get_stored_reports():
        click.confirm('Do you want to overwrite %s?' % target,
                      abort=True)

    config.copy_report(source, target)


@main.command()
@click.option('--template', '-t', required=False)
@click.pass_obj
def edit(config, template):
    if template:
        template_file = os.path.join(click.get_app_dir('hreports'),
                                     'templates',
                                     template)

        if not os.path.exists(os.path.dirname(template_file)):
                os.makedirs(os.path.dirname(template_file))

        click.edit(filename=template_file)
    else:
        click.edit(filename=config.cfg_file)


@click.argument('name')
@main.command()
@click.option('--file-type', '-f', required=False,
              type=click.Choice(['md', 'pdf', 'html']))
@click.pass_obj
def save(config, name, **meta):
    hreport = hreports.Hreport(config)
    output_file = hreport.save(name)
    click.echo('Saved %s' % output_file)


if __name__ == "__main__":
    main()
