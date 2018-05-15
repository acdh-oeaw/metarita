import re
import pandas as pd
from entities.models import *
from relations.models import *
from vocabularies.models import *


def clean_place_string(place_string):

    """ takes e.g. 'St. Lorenzen (St. Michaelsburg)' and
    returns the tuple ('St. Lorenzen', 'St Michaelsburg') """

    first_place = place_string.split("(")[0]
    lg = " ".join(place_string.split("(")[1:])
    lg = lg.replace(')', '')
    return(first_place, lg)


def create_places_from_place_string(place_string):

    """ takes e.g. 'St. Lorenzen (St. Michaelsburg)' creates two place objects,
    relates them 'part_of' and returns a tuple containing those two places."""

    cleaned = clean_place_string(place_string)
    first_second, _ = PlacePlaceRelation.objects.get_or_create(
        name="part of",
        name_reverse="has part"
    )
    if len(cleaned) == 2:
        first, _ = Place.objects.get_or_create(
            name=cleaned[0]
        )
        second, _ = Place.objects.get_or_create(
            name=cleaned[1]
        )
        relate_places = PlacePlace.objects.get_or_create(
            relation_type=first_second,
            related_placeA=first,
            related_placeB=second
        )
        return (first, second)


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
