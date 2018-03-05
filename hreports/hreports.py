# -*- coding: utf-8 -*-

"""Main module."""

import os
import io
import subprocess
import datetime
import tempfile
import shlex
from jinja2 import Environment, ChoiceLoader, \
    FileSystemLoader, PackageLoader, select_autoescape
from jinja2.exceptions import TemplateSyntaxError, TemplateNotFound, \
    UndefinedError
from .template_filters import datetimeformat, german_float, \
    last_day_of_month, substract_days, multiply_last_column, \
    add_percentage_column


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
        self.env.filters['last_day_of_month'] = last_day_of_month
        self.env.filters['substract_days'] = substract_days
        self.env.filters['multiply_last_column'] = multiply_last_column
        self.env.filters['add_percentage_column'] = add_percentage_column

    def get_global_config(self):
        return self.config.data.get('global', None)

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

    def run(self, name=False, query=False, ledger=False):
        if name:
            query = self.get_report_config_value(name, 'query')
            ledger = self.get_report_config_value(name, 'ledger')

        if not ledger:
            ledger = self.get_global_config_value('ledger')

        query = self.render_string(query, name)

        if ledger:
            cmd = 'hledger -f %s %s' % (ledger, query)
        else:
            cmd = 'hledger %s' % query
        self.config.cmd = cmd
        try:
            cmd_list = shlex.split(cmd)
            output = unicode(subprocess.check_output(cmd_list), 'utf-8')
            self.config.returncode = 0
        except subprocess.CalledProcessError as exception:
            self.config.error = exception.output
            self.config.returncode = exception.returncode
            output = 'Query %s returned non-zero exit status' % cmd
        return output

    def render_string(self, string, name=False):
        string_template = self.env.from_string(string)
        try:
            string = string_template.render(self.get_context(name))
        except TemplateSyntaxError:
            string = 'Encountered syntax error in %s' % string
        except UndefinedError as exception:
            string = 'Encountered variable UndefinedError: %s' % \
                exception.message
        return string

    def render_strings_in_dict(self, data_dict, context, section=False):
        if not data_dict:
            return context
        for key, value in data_dict.items():
            if isinstance(value, str):
                value_template = self.env.from_string(value)
                data_dict[key] = value_template.render(context)
        if section:
            context.update({section: data_dict})
        else:
            context.update(data_dict)
        return context

    def get_context(self, name=False):
        """Build context data for the template.

        The template context dict is evaluated in this order:

            1. Builtins at {}
            2. variables of the global section at {}
            3. global section at {'global'}
            4. variables of the report section {'report'}
            5 report section at {}
        """
        context = {}

        builtins = {'now': datetime.datetime.now()}
        context.update(builtins)

        global_config = self.get_global_config()
        if 'variables' in global_config:
            global_variables = global_config.get('variables', {})
            context = self.render_strings_in_dict(global_variables,
                                                  context)
        self.render_strings_in_dict(global_config, context, 'global')

        report_config = self.get_report_config(name)
        if report_config:
            report_variables = report_config.get('variables', {})
            self.render_strings_in_dict(report_variables, context)

        self.render_strings_in_dict(report_config, context, 'report')

        context.update({'hreport': self})

        return context

    def render(self, name):

        template_name = self.get_report_config_value(name, 'template')

        if not template_name:
            return self.run(name)

        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            result = 'Template %s Not Found' % template_name
            return result
        except TemplateSyntaxError:
            result = 'Template syntax error in %s' % template_name
            return result

        context = self.get_context(name)
        context['output'] = self.run(name).splitlines()

        try:
            result = template.render(context)
        except TemplateSyntaxError:
            result = 'Template raised error: "%s"' % template
        except UndefinedError as exception:
            result = 'Variable UndefinedError %s in template "%s"' % \
                (exception.message, template_name)
        return result

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

        output_file = self.render_string(output_file, name)

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
        cmd_list = shlex.split(cmd)
        unicode(subprocess.check_output(cmd_list), 'utf-8')
        os.unlink(input_file.name)
        return output_file
