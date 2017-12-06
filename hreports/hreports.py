# -*- coding: utf-8 -*-

"""Main module."""

import subprocess
from jinja2 import Environment, ChoiceLoader, \
    FileSystemLoader, PackageLoader, select_autoescape


class Hreport(object):
    def __init__(self, config, name=False):
        self.config = config
        self.name = name

    def get_report_config_value(self, key):
        report_config = self.config.data.get('reports').get(self.name)
        value = report_config.get(key, None)
        if not value:
            # Try general section
            return self.config.data.get('general').get(key)
        return value

    def get_report_config(self):
        return self.config.data.get('reports').get(self.name, None)

    def run(self, query=False):
        if not query:
            query = self.get_report_config_value('query')
            print(query)
        ledger = self.get_report_config_value('ledger')
        if ledger:
            cmd = 'hledger -f %s %s' % (ledger, query)
        else:
            cmd = 'hledger %s' % query
        output = subprocess.check_output(cmd.split(' '))
        return output

    def render(self, template_name=None):

        if not template_name:
            template_name = self.get_report_config_value('template_name')

        if not template_name:
            return self.run()

        loader = ChoiceLoader([
                    FileSystemLoader('./'),
                    FileSystemLoader('/templates'),
                    PackageLoader('hreports', 'templates'),
        ])
        env = Environment(loader=loader,
                          autoescape=select_autoescape(['html', 'xml'])
                          )

        template = env.get_template(template_name)
        context = self.get_report_config()
        context['output'] = self.run().splitlines()
        return template.render(context)
