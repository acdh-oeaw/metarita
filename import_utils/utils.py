import re
import pandas as pd


def get_filtered_sheets(file, filterstring='V'):
    """ returns a list of sheet names containing the filterstring value """
    sheets = pd.read_excel(file, None).keys()
    filtered = [x for x in sheets if x.startswith(filterstring)]
    return {'sheets': sheets, 'filtered': filtered}


def first_row_item(df, key):
    first_row_items = []
    for x in df[key].iteritems():
        first_row_items.append(x[1].split('\n')[0])
    return first_row_items


def first_cell_items(df, key, delimiter='\n'):
    cell_items = []
    for x in df[key].iteritems():
        cell_items.append(x[1].split(delimiter)[0])
    return cell_items


def get_dfs(file, filterstring='V'):
    return [
        pd.read_excel(file, x).fillna('FALSE') for x in get_filtered_sheets(
            file, filterstring
            )['filtered']
        ]
