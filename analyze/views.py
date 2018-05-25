from collections import Counter
import pandas as pd

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
        return context
