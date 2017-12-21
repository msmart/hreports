# -*- coding: utf-8 -*-

import datetime


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def german_float(value):
    value = float(value)
    return '{:,.2f}'.format(value).replace(",", "X")\
                    .replace(".", ",").replace("X", ".")


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)
