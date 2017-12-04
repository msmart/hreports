# -*- coding: utf-8 -*-

"""Main module."""

import subprocess


class Create(object):
    def __init__(self, name=None, query=None):
        self.name = name
        self.query = query

    def run(self):
        cmd = 'hledger %s' % self.query
        output = subprocess.check_output(cmd.split(' '))
        return output
