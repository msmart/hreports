#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hreports` package."""


import unittest

from hreports import template_filters
from datetime import datetime
from jinja2.exceptions import FilterArgumentError


class TestHreportsTemplateFilters(unittest.TestCase):
    """Tests for `hreports` package."""

    def test_german_float(self):
        value = template_filters.german_float("2.0")
        assert '2,0' in value

        value = template_filters.german_float("2000.00")
        assert '2.000,00' in value

    def test_datetimeformat(self):
        dt = datetime(year=2000, month=12, day=31, hour=14, minute=20)
        value = template_filters. datetimeformat(dt, format='%H:%M / %d-%m-%Y')
        assert '14:20 / 31-12-2000' in value

    def test_lastdayofmontht(self):
        dt = datetime(year=2000, month=12, day=12, hour=14, minute=20)
        value = template_filters.last_day_of_month(dt)
        assert value.day == 31

    def test_substract_days(self):
        dt = datetime(year=2000, month=12, day=12, hour=14, minute=20)
        value = template_filters.substract_days(dt, 14)
        assert value.day == 28
        assert value.month == 11

        dt = datetime(year=2000, month=12, day=12, hour=14, minute=20)
        value = template_filters.substract_days(dt, -4)
        assert value.day == 16
        assert value.month == 12

    def test_calculate_last_column(self):
        line = "account | 123 | 34 |"
        keywords = {'account': '2'}
        value = 23
        factor = 4
        res = template_filters.calculate_last_column(line, value,
                                                     factor, keywords)
        assert "46.00" in res

        line = "another | 123 | 34 |"
        res = template_filters.calculate_last_column(line, value,
                                                     factor, keywords)

        assert "92.00" in res

    def test_parse_multiply_last_column_input(self):
        factor = 2
        keywords = [['a', '2'], ['b', '3']]
        r = template_filters.parse_multiply_last_column_input(factor, keywords)
        assert isinstance(r[1], dict)

        keywords = None
        r = template_filters.parse_multiply_last_column_input(factor, keywords)
        assert r[1] == {}

        keywords = None
        factor = 'a'
        with self.assertRaises(FilterArgumentError):
            r = template_filters.parse_multiply_last_column_input(factor,
                                                                  keywords)

        keywords = [['a'], ['b', '3']]
        factor = '2'
        with self.assertRaises(FilterArgumentError):
            r = template_filters.parse_multiply_last_column_input(factor,
                                                                  keywords)
