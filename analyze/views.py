from collections import Counter
import pandas as pd

from django.db.models import Avg, Sum, Count
from django.shortcuts import render
from django.views.generic import TemplateView

from relations.models import *
from entities.models import *


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
