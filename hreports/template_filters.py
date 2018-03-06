# -*- coding: utf-8 -*-

import datetime
from jinja2.exceptions import FilterArgumentError


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def german_float(value):
    value = float(value)
    return '{:,.2f}'.format(value).replace(",", "X")\
                    .replace(".", ",").replace("X", ".")


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def substract_days(any_day,  amount):
    if amount < 0:
        new_date = any_day + datetime.timedelta(days=-1*amount)
    else:
        new_date = any_day - datetime.timedelta(days=amount)
    return new_date


def parse_multiply_last_column_input(factor, keywords):
    factor_by_keyword = {}
    if isinstance(keywords, list):
        try:
            for keyword in keywords:
                factor_by_keyword[keyword[0]] = keyword[1]
        except TypeError:
            raise FilterArgumentError
    else:
        try:
            factor = float(factor)
        except ValueError:
            raise FilterArgumentError
    return factor, factor_by_keyword


def calculate_last_column(line, value, factor, keywords):
    result = None
    if keywords:
        for keyword in keywords.keys():
            if keyword in line:
                factor = float(keywords.get(keyword))
                return '{:,.2f}'.format(value*factor)
    if not result:
        return '{:,.2f}'.format(value*factor)


def multiply_last_column(output, factor, title=None, keywords={}):
    max_length = max([len(x) for x in output])
    factor, keywords = parse_multiply_last_column_input(factor, keywords)

    extra_column = []

    # Split each line and find the last string that converts to a float
    for line in output:
        result = None
        columns = line.split(' ')
        columns.reverse()
        for cell in columns:
            try:
                cell = cell.replace(",", "")
                value = float(cell)
                result = calculate_last_column(line, value, factor, keywords)
                if result:
                    extra_column.append(result)
                    break
            except ValueError:
                value = cell

        # Append space if no float was found in line
        if not result:
            extra_column.append(" ")

    # Replace first instance with title
    if title:
        floats = [i for i, f in enumerate(extra_column) if f != " "]
        if floats:
            extra_column[floats[0]] = title

        # Special case for the percentage filter
        if title == "%":
            return extra_column

    # Append to existing output and align spacing
    max_result_value = max([len(x) for x in extra_column])
    output_with_extra_column = []

    for line, column in zip(output, extra_column):
        new_line = line + " "*(max_length-len(line)) + " " +\
                   " "*(max_result_value-len(column)) + column
        output_with_extra_column.append(new_line)

    return output_with_extra_column


def add_percentage_column(output):
    extra_column = multiply_last_column(output, 1.0, "%", {})
    floats = [i for i, f in enumerate(extra_column) if f != " "]
    for index in floats[1:]:
        extra_column[index] = float(extra_column[index].replace(',', ''))
    total = extra_column[floats[-1]]

    total_percentage = 0
    for index in floats[1:-1]:
        percentage = 100*(extra_column[index]/total)
        total_percentage += percentage
        extra_column[index] = '{:,.2f}'.format(percentage)
    extra_column[floats[-1]] = '{:,.2f}'.format(total_percentage)

    max_result_value = max([len(x) for x in extra_column])
    output_with_extra_column = []
    max_length = max([len(x) for x in output])
    for line, column in zip(output, extra_column):
        new_line = line + " "*(max_length-len(line)) + " " +\
                   " "*(max_result_value-len(column)) + column
        output_with_extra_column.append(new_line)

    return output_with_extra_column
