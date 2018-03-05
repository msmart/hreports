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
        except:
            raise Exception
    else:
        try:
            factor = float(factor)
        except:
            raise Exception
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
            except:
                value = cell

        # Append space if not float was found in line
        if not result:
            extra_column.append(" ")

    # Replace first instance with title
    if title:
        floats = [i for i, f in enumerate(extra_column) if f != " "]
        if floats:
            extra_column[floats[0]] = title

    max_result_value = max([len(x) for x in extra_column])
    output_with_extra_column = []

    for line, column in zip(output, extra_column):
        new_line = line + " "*(max_length-len(line)) + " " +\
                   " "*(max_result_value-len(column)) + column
        output_with_extra_column.append(new_line)

    return output_with_extra_column
