import re
import pandas as pd


def get_vb_sheets(file, filterstring='V'):
    sheets = pd.read_excel(file, None).keys()
    filtered = [x for x in sheets if x.startswith(filterstring)]
    return {'sheets': sheets, 'filtered': filtered}


def first_row_item(df, key):
    first_row_items = []
    for x in df[key].iteritems():
        first_row_items.append(x[1].split('\n')[0])
    return first_row_items


def get_dfs(file):
    return [pd.read_excel(file, x) for x in get_vb_sheets(file)['filtered']]
