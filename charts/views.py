import json
from django_tables2 import SingleTableView, RequestConfig
from django.views.generic import TemplateView
from django.db.models import Count
from django.views.generic.list import ListView
from .models import ChartConfig
from entities.models import Work


class ChartSelector(ListView):
    model = ChartConfig
    template_name = 'charts/select_chart.html'


class DynChartView(TemplateView):

    template_name = 'charts/dynchart.html'

    def get_context_data(self, **kwargs):
        context = super(DynChartView, self).get_context_data()
        property_name = self.kwargs['property']
        context['property_name'] = property_name
        try:
            chart = ChartConfig.objects.get(
                field_path=self.kwargs['property']
            )
        except:
            context['error'] = True
            return context

        context['charttype'] = self.kwargs['charttype']
        modelname = Work
        payload = []
        objects = Work.objects.all()
        for x in objects.values(property_name).annotate(
                amount=Count(property_name)).order_by(property_name):
            if x[property_name]:
                payload.append(["{}".format(x[property_name]), x['amount']])
            else:
                payload.append(['None', x['amount']])
        context['all'] = objects.count()
        if chart.legend_x:
            legendx = chart.legend_x
        else:
            legendx = "# of {}s".format(modelname)
        data = {
            "items": "{} out of {}".format(objects.count(), context['all']),
            "title": "{}".format(chart.label),
            "subtitle": "{}".format(chart.help_text),
            "legendy": chart.legend_y,
            "legendx": legendx,
            "categories": "sorted(dates)",
            "measuredObject": "{}s".format(modelname),
            "ymin": 0,
            "payload": payload
        }
        context['data'] = data

        return context
