from django.http import JsonResponse
from collections import Counter
import pandas as pd
from datetime import date, timedelta
from django.urls import reverse
from django.db.models import Avg, Sum, Count
from django.shortcuts import render
from django.views.generic import TemplateView

from relations.models import *
from entities.models import *


def make_href(row, entity='work', id='id', label=None):
    url = reverse(
        'entities:generic_entities_detail_view',
        kwargs={'pk': row[id], 'entity': entity}
    )
    if label:
        element = """<a href="{}" target='_blank'>{}</a>""".format(url, row[label])
    else:
        element = """<a href="{}" target='_blank'>{}</a>""".format(url, 'link2object')
    return element


def calculate_duration(row):
    if row['end_date'] and row['start_date']:
        time = pd.to_timedelta(
            (row['end_date']-row['start_date']) + timedelta(days=1)
        ).__str__()
    else:
        time = pd.to_timedelta("0 days").__str__()
    return time


def get_datatables_data(request):
    pd.set_option('display.max_colwidth', -1)

    # PersonWorkRelation
    queryset = list(
        PersonWork.objects.values(
            'id',
            'relation_type__name',
            'related_work__name',
            'related_work__id',
            'related_person__name',
            'related_person',
            'start_date',
            'end_date',
        )
    )
    df = pd.DataFrame(queryset)
    df['related_work__name'] = df.apply(
        lambda row: make_href(
            row, entity='work',
            id='related_work__id',
            label='related_work__name'
        ), axis=1
    )
    df['involved_pers'] = df.groupby('related_work__name')['related_work__name']\
        .transform('count')
    df['grouped_by_pers'] = df.groupby('involved_pers')['involved_pers'].transform('count')
    df['grouped_by_pers'] = (df['grouped_by_pers'] / df['involved_pers'])
    df['involved_works'] = df.groupby('related_person')['related_person']\
        .transform('count')
    df['grouped_by_works'] = df.groupby('involved_works')['involved_works'].transform('count')
    df['grouped_by_works'] = (df['grouped_by_works'] / df['involved_works'])
    df['duration'] = df.apply(lambda row: calculate_duration(row), axis=1)
    df['duration'] = df.apply(lambda row: calculate_duration(row), axis=1)
    payload = {}
    payload['data'] = df.values.tolist()
    payload['columns'] = list(df)
    return JsonResponse(payload)


class WorkAnalyze(TemplateView):
    template_name = "analyze/basic.html"
