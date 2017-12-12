# -*- coding: utf-8 -*-

"""Config object for hreports."""

import os
import copy
import yaml
import click


APP_NAME = 'hreports'


class Config(object):

    def __init__(self):
        self.verbose = False
        self.data = {'global': {}, 'reports': {}}
        self.read_config()

    def get_stored_reports(self):
        return self.data.get('reports')

    def store_report_data(self, name, data):
        if name not in self.data.get('reports').keys():
            self.data.get('reports')[name] = {}

        # Remove none value
        data_dict = {}
        for key, value in data.items():
            if value:
                data_dict[key] = value

        self.data.get('reports')[name].update(data_dict)

    def delete_report(self, name):
        if name in self.data.get('reports').keys():
            self.data.get('reports').pop(name)
        self.write_config()

    def copy_report(self, source, target):
        source_config = self.data.get('reports').get(source)
        click.echo(source_config)
        if source_config:
            target_config = copy.deepcopy(source_config)
            self.data.get('reports')[target] = target_config
        self.write_config()

    def update_report(self, name, meta=False, variables=False):
        if meta:
            self.store_report_data(name, meta)
        if variables:
            report_config = self.data.get('reports').get(name)
            section_dict = report_config.get('variables', {})
            for key, value in variables:
                section_dict[key] = value
                self.store_report_data(name, {'variables': section_dict})

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

            if cfg.get('meta', None) and cfg.get('meta').get('desc', None):
                click.secho(report.ljust(report_name_length),
                            fg='green', nl=False)
                click.secho(' -- %s' % cfg.get('meta').get('desc'),
                            )
            else:
                click.secho('%s' % report, fg='green')
