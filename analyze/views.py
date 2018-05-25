from collections import Counter
import pandas as pd
from datetime import date, timedelta

from django.db.models import Avg, Sum, Count
from django.shortcuts import render
from django.views.generic import TemplateView

from relations.models import *
from entities.models import *


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
            lambda row: "{}".format((row['end_date']-row['start_date']) + timedelta(days=1)), axis=1
        )
        df['occurences'] = df.groupby('duration')['duration'].transform(pd.Series.value_counts)
        context['duration_table'] = df.sort_values('duration').to_html(classes=['table'])
        # by_duration = df.groupby('duration').count()
        # context['duration_max'] = by_duration['end_date'].max()
        # context['duration_min'] = by_duration['end_date'].min()
        # context['duration_mean'] = by_duration['end_date'].mean()
        return context
