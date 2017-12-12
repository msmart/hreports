# -*- coding: utf-8 -*-

"""Main module."""

import os
import io
import subprocess
import datetime
import tempfile
from jinja2 import Environment, ChoiceLoader, \
    FileSystemLoader, PackageLoader, select_autoescape
from .template_filters import datetimeformat, german_float


class Hreport(object):
    def __init__(self, config):
        self.config = config

        cfg_path = os.path.dirname(self.config.cfg_file)
        self.cfg_templates = os.path.join(cfg_path, 'templates')

        loader = ChoiceLoader([
                    FileSystemLoader('./'),
                    FileSystemLoader('/templates'),
                    FileSystemLoader(self.cfg_templates),
                    PackageLoader('hreports', 'templates'),
        ])
        self.env = Environment(loader=loader,
                               autoescape=select_autoescape(['html', 'xml'])
                               )

        self.env.filters['datetime'] = datetimeformat
        self.env.filters['german_float'] = german_float

    def get_report_config(self, name):
        return self.config.data.get('reports').get(name, None)

    def get_report_config_value(self, name, key):
        report_config = self.config.data.get('reports').get(name, None)
        if report_config:
            value = report_config.get(key, None)
        else:
            value = False
        if not value:
            # Try global section
            return self.get_global_config_value(value)
        return value

    def get_global_config_value(self, key):
        return self.config.data.get('global').get(key, None)

    def get_output(self, query, ledger=False):
        if ledger:
            cmd = 'hledger -f %s %s' % (ledger, query)
        else:
            cmd = 'hledger %s' % query
        return unicode(subprocess.check_output(cmd.split(' ')), 'utf-8')

    def run_query(self, query, ledger=False):
        if not ledger:
            ledger = self.get_global_config_value('ledger')
        query = self.env.from_string(query)
        query = query.render(self.get_context())
        return self.get_output(query, ledger)

    def run(self, name):
        query = self.get_report_config_value(name, 'query')
        ledger = self.get_report_config_value(name, 'ledger')
        return self.run_query(query, ledger)

    def get_context(self, name=False):
        builtins = {'now': datetime.datetime.now()}
        report_config = self.get_report_config(name)
        context = {'report': report_config,
                   'hreport': self,
                   'global': self.config.data.get('global')}

        context.update(builtins)
        if report_config:
            context.update(report_config.get('variables', {}))
        return context

    def render(self, name, template_name=None):

        if not template_name:
            template_name = self.get_report_config_value(name,
                                                         'template')
        if not template_name:
            return self.run(name)

        template = self.env.get_template(template_name)
        context = self.get_context(name)
        context['output'] = self.run(name).splitlines()
        return template.render(context)

    def save(self, name):
        input_file = tempfile.NamedTemporaryFile(dir='.',
                                                 delete=False)
        input_file.close()

        with io.open(input_file.name, 'w',
                     encoding='utf-8') as input_file:
            input_file.write(self.render(name))
        output_file = self.get_report_config_value(name, 'filename')

        if not output_file:
            output_file = '%s.pdf' % name

        output_file_template = self.env.from_string(output_file)
        context = self.get_context(name)
        output_file = output_file_template.render(context)

        cmd = 'pandoc %s -t html5 -o %s' % (input_file.name,
                                            output_file)

        styling = self.get_report_config_value(name, 'styling')
        template_name = self.get_report_config_value(name,
                                                     'template')
        if styling:
            styling = os.path.join(self.cfg_templates, styling)
            styling = '--css "%s"' % styling
        elif template_name:
            styling_default = template_name.split('.')[0] + '.css'
            styling_default_path = os.path.join(self.cfg_templates,
                                                styling_default)
            if os.path.exists(styling_default_path):
                cmd = cmd + ' --css %s' % styling_default_path
        input_file.close()
        unicode(subprocess.check_output(cmd.split(' ')), 'utf-8')
        os.unlink(input_file.name)
        return output_file
