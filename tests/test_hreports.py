#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hreports` package."""

import os
import unittest
import logging
import tempfile
from click.testing import CliRunner

from hreports import cli, hreports

logger = logging.getLogger()


class TestHreports(unittest.TestCase):
    """Tests for `hreports` package."""

    @classmethod
    def setUp(self):
        self.config_file = tempfile.NamedTemporaryFile()
        self.config_file.flush()
        self.cfg_arg = ['-c', self.config_file.name]
        self.runner = CliRunner()

    @classmethod
    def tearDown(self):
        self.config_file.close()

    def test_command_line_interface(self):
        """Test the CLI."""
        result = self.runner.invoke(cli.main, ['-c', 'aa'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn('does not exist', result.output)

    def test_custom_empty_config(self):
        result = self.runner.invoke(cli.main, self.cfg_arg)
        self.assertIn('No reports saved', result.output)
        self.assertEqual(result.exit_code, 0)

    def test_show_help(self):
        args = ['--help']
        help_result = self.runner.invoke(cli.main, args)
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_create_and_show_report(self):
        args = ['--verbose', 'create', 'test_report']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertIn(self.config_file.name, result.output)
        self.assertIn('test_report', result.output)
        self.assertEqual(result.exit_code, 0)

        args = ['--verbose', '-r', 'test_report']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('test_report contains no configuration',
                      result.output)

        args = ['--verbose', 'update', 'test_report', '-q "balance XY"']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Updating  test_report',
                      result.output)

        args = ['--verbose', '-r', 'test_report']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('balance XY',
                      result.output)

    def test_create_and_copy_report(self):
        args = ['--verbose', 'create', 'test_report2', '-q "reg ZX"']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertIn('test_report2', result.output)
        self.assertEqual(result.exit_code, 0)

        args = ['--verbose', 'copy', 'test_report2', 'copy_report']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)

        args = ['--verbose', '-r', 'copy_report']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('reg ZX',
                      result.output)

        args = ['--verbose', 'copy', 'non_existent', 'copy_report']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Error: Report', result.output)

    def test_delete_report(self):
        args = ['--verbose', 'create', 'test3', '-q "reg ZX"']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertIn('test3', result.output)

        args = ['--verbose', 'delete', 'test3']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)

        args = ['--verbose']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn('test3', result.output)

        args = ['--verbose', 'delete', 'test3']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 2)
        self.assertIn('Report test3 does not exist', result.output)

    def test_show_report(self):
        args = ['--verbose', 'create', 'test3', '-q "bal"']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        assert not result.exception

        self.assertEqual(result.exit_code, 0)
        self.assertIn('test3', result.output)
        ledger = tempfile.NamedTemporaryFile(mode='w')
        ledger.write('2010/1/12 *\n    income  243\n    asset   \n')
        ledger.flush()
        args = ['--verbose', 'show', 'test3', '-l', ledger.name]

        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        assert not result.exception
        self.assertIn('243', result.output)
        self.assertEqual(result.exit_code, 0)
        ledger.close()

    def test_save_report(self):
        args = ['--verbose', 'create', 'test3', '-q "bal"']
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        assert not result.exception
        self.assertEqual(result.exit_code, 0)
        self.assertIn('test3', result.output)

        ledger = tempfile.NamedTemporaryFile(mode='w', delete=False)
        ledger.write('2010/1/12 *\n    income  2\n    asset  \n')
        args = ['--verbose', 'show', 'test3', '-l', ledger.name]
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        self.assertEqual(result.exit_code, 0)

        args = ['save', 'test3', '-l', ledger.name]
        result = self.runner.invoke(cli.main, self.cfg_arg + args)
        assert not result.exception
        assert os.path.isfile('test3.pdf')
        self.assertNotEqual(os.stat('test3.pdf').st_size, 0)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('test3', result.output)

    def test_get_global_config(self):
        from hreports import config
        test = config.Config(self.config_file.name)
        hreport = hreports.Hreport(test)
        config = hreport.get_global_config()
        self.assertIsInstance(config, dict)
