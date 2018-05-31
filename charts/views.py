import json
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, FieldError
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
        model_name = self.kwargs['model_name']
        try:
            ct = ContentType.objects.get(model=model_name).model_class()
        except ObjectDoesNotExist:
            context['fatal_error'] = True
            context['error_msg'] = "The model: <code>{}</code> you requested is not defined"\
                .format(model_name.title())
            return context

        property_name = self.kwargs['property']
        context['property_name'] = property_name
        try:
            chart = ChartConfig.objects.get(
                field_path=property_name,
                model_name=model_name
            )
            chart = chart.__dict__
        except ObjectDoesNotExist:
            context['error'] = True
            context['error_msg'] = """The ChartConfig Object:
                <code>field_path={}, model_name={}</code> you requested couldn't be found."""\
                .format(property_name, model_name.title())
            chart = {
                'legend_x': None,
                'legend_y': None,
                'label': 'not defined',
                'help_text': 'not defined'
            }

        context['charttype'] = self.kwargs['charttype']
        modelname = ct.__name__
        payload = []
        objects = ct.objects.all()
        try:
            for x in objects.values(property_name).annotate(
                    amount=Count(property_name)).order_by(property_name):
                if x[property_name]:
                    payload.append(["{}".format(x[property_name]), x['amount']])
                else:
                    payload.append(['None', x['amount']])
            context['all'] = objects.count()
            if chart['legend_x']:
                legendx = chart['legend_x']
            else:
                legendx = "# of {}s".format(modelname)
            data = {
                "items": "{} out of {}".format(objects.count(), context['all']),
                "title": "{}".format(chart['label']),
                "subtitle": "{}".format(chart["help_text"]),
                "legendy": chart["legend_y"],
                "legendx": legendx,
                "categories": "sorted(dates)",
                "measuredObject": "{}s".format(modelname),
                "ymin": 0,
                "payload": payload
            }
            context['data'] = data
        except FieldError:
            context['error'] = True
            context['error_msg'] = "The field: <code>{}</code> you requested does not exist"\
                .format(property_name)

        return context
