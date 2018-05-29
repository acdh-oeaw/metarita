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
            "{}".format((row['end_date']-row['start_date']) + timedelta(days=1))
        )
    else:
        time = pd.to_timedelta("0 days")
    return time


def get_works_by_rel_person(num_rel_persons):
    queryset = list(
        PersonWork.objects.values('related_work').annotate(rel_persons=Count('related_person'))
    )
    works = [
        Work.objects.get(id=x['related_work'])
        for x in queryset if x['rel_persons'] == int(num_rel_persons)
    ]
    return queryset, sorted(works)


class SelectedSample(TemplateView):
    template_name = "analyze/sample.html"

    def get_context_data(self, **kwargs):
        context = super(SelectedSample, self).get_context_data()
        num_rel_persons = self.kwargs['pk']
        works = get_works_by_rel_person(num_rel_persons)
        context['works'] = works[1]
        return context


class WorkAnalyze(TemplateView):
    template_name = "analyze/basic.html"

    def get_context_data(self, **kwargs):
        context = super(WorkAnalyze, self).get_context_data()
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
        df['duration'] = df.apply(lambda row: calculate_duration(row), axis=1)
        context['PersonWork_table'] = df.to_html(
            classes=['table'], escape=False, table_id='PersonWork_table'
        )
        return context
