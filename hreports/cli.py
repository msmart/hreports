# -*- coding: utf-8 -*-

"""Console script for hreports."""

import os
import click
import yaml

import hreports
from .config import Config


def composed(*decs):
    """Combine multiple decorators.
    See https://stackoverflow.com/questions/5409450/
    """

    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


common = composed(click.option('--query', '-q', required=False),
                  click.option('--template', '-t', required=False),
                  click.option('--filename', '-f', required=False),
                  click.option('--ledger', '-l', required=False),
                  click.option('--desc', '-d', required=False),
                  click.option('--variables', '-var', required=False,
                               type=(str, str), multiple=True)
                  )


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
@click.option('--config-file', '-c', required=False,
              type=click.Path(exists=True),
              help='Use config file')
@click.option('--config-info', '-i', is_flag=True,
              help='Show current config file')
@click.option('--verbose', is_flag=True)
@click.option('--query', '-q', required=False,
              metavar='QUERY',
              help='Execute QUERY query')
@click.option('--report-config', '-r', required=False,
              metavar='REPORT',
              help='Show configuration of REPORT')
@click.option('--ledger', '-l', metavar='FILE', required=False,
              type=click.Path(exists=True),
              help='Use FILE ledger')
@click.version_option()
@click.pass_context
def main(context, config_info, config_file, ledger, verbose,
         query, report_config):
    """Manage hledger queries."""
    config = Config()
    context.obj = config
    click.echo(ledger)
    context.obj.ledger = ledger

    if verbose:
        config.verbose = True
        click.echo("Config file %s" % config.cfg_file)
    if not context.invoked_subcommand and query:
        hreport = hreports.Hreport(config)
        click.echo("Running %s" % query)
        click.echo(hreport.run(query=query))
    elif report_config:
        report_config = config.get_stored_reports().get(report_config)
        click.echo(yaml.dump(report_config, default_flow_style=False))
    elif config_info:
        print(yaml.dump(config.data))
    elif not context.invoked_subcommand:
        config.echo_saved_reports()


@main.command(short_help='Create a report')
@click.argument('name')
@common
@click.pass_obj
def create(config, name, variables, **meta):
    click.echo('Saving %s report' % name)
    if name in config.get_stored_reports():
        click.confirm('Do you want to overwrite %s?' % name,
                      abort=True)
        config.delete_report(name)
    config.update_report(name, meta, variables)


@main.command(short_help='Update report configuration')
@click.argument('name')
@common
@click.pass_obj
def update(config, name, variables, **meta):
    click.echo('Updating  %s report' % name)
    config.update_report(name, meta, variables)


@main.command(short_help='Delete report')
@click.argument('name')
@click.pass_obj
def delete(config, name):
    if name not in config.get_stored_reports():
        raise click.UsageError('Report %s does not exist.' % name)
    else:
        click.echo('Deleting %s report' % name)
        config.delete_report(name)


@main.command(short_help='Show report result')
@click.argument('name', required=False)
@common
@click.pass_obj
def show(config, name, variables, **meta):

    if config.verbose:
        click.echo("Showing reports", nl=True)

    if not name or name not in config.get_stored_reports():
        config.echo_saved_reports()
    elif name:
        config.update_report(name, meta=meta, variables=variables,
                             write=False)
        hreport = hreports.Hreport(config)
        click.echo(hreport.render(name))

        if config.verbose:
            click.echo('Ran query "%s"' % config.cmd)


@main.command(short_help='Copy report configuration')
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


@main.command(short_help='Edit configuration file or template')
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
@main.command(short_help='Save report to pdf file')
@common
@click.option('--file-type', '-f', required=False,
              type=click.Choice(['md', 'pdf', 'html']))
@click.pass_obj
def save(config, name, variables, **meta):
    config.update_report(name, meta, variables)
    hreport = hreports.Hreport(config)
    output_file = hreport.save(name)
    click.echo('Saved %s' % output_file)


if __name__ == "__main__":
    main()
