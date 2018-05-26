from collections import Counter
import pandas as pd
from datetime import date, timedelta
from django.urls import reverse
from django.db.models import Avg, Sum, Count
from django.shortcuts import render
from django.views.generic import TemplateView

from relations.models import *
from entities.models import *


def make_href(row):
    url = reverse(
        'entities:generic_entities_detail_view',
        kwargs={'pk': row['id'], 'entity': 'work'}
    )
    element = """<a href="{}">{}</a>""".format(url, row['id'])
    return element


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
        queryset = list(
            PersonWork.objects.values('related_work__name')
            .annotate(rel_persons=Count('related_person'))
        )
        df = pd.DataFrame(queryset)
        by_rel_pers = df.groupby('rel_persons').count()
        context['rows'] = [[i for i in row] for row in by_rel_pers.itertuples()]
        context['relations'] = len(queryset)
        context['mean'] = df['rel_persons'].mean()
        context['max'] = df['rel_persons'].max()
        context['min'] = df['rel_persons'].min()
        queryset = list(
            Work.objects.exclude(kind__name='Verfachbuch')
            .exclude(start_date__isnull=True)
            .values('name', 'id', 'start_date', 'end_date'))
        df = pd.DataFrame(queryset)
        df['duration'] = df.apply(
            lambda row: pd.to_timedelta(
                "{}".format((row['end_date']-row['start_date']) + timedelta(days=1))
            ), axis=1
        )
        df['id'] = df.apply(lambda row: make_href(row), axis=1)
        df['occurences'] = df.groupby('duration')['duration'].transform(pd.Series.value_counts)
        context['duration_table'] = df.sort_values('duration').to_html(
            classes=['table'], escape=False, table_id='duration_table'
        )
        context['duration_max'] = df['duration'].max()
        context['duration_min'] = df['duration'].min()
        context['duration_mean'] = df['duration'].mean()
        return context
