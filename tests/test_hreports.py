#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hreports` package."""


import unittest
import tempfile
from click.testing import CliRunner

from hreports import cli, hreports


class TestHreports(unittest.TestCase):
    """Tests for `hreports` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'reports' in result.output

        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

        show_result = runner.invoke(cli.main, ['show'])
        self.assertEqual(show_result.exit_code, 0)
        self.assertIn('reports', show_result.output)

    def test_config(self):
        runner = CliRunner()
        config = tempfile.NamedTemporaryFile()

        runner.invoke(cli.main, ['-c', config.name, 'create', 'test'])
        result = runner.invoke(cli.main, ['-c', config.name,
                                          '--verbose', '-r'])
        self.assertIn(config.name, result.output)

    def test_get_global_config(self):
        from hreports import config
        test = config.Config()
        hreport = hreports.Hreport(test)
        config = hreport.get_global_config()
        self.assertIsInstance(config, dict)
