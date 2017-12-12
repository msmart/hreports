# -*- coding: utf-8 -*-


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def german_float(value):
    value = float(value)
    return '{:,.2f}'.format(value).replace(",", "X")\
                    .replace(".", ",").replace("X", ".")
