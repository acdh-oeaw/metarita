from django import template
from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.inclusion_tag('charts/tags/load_highcharts_js.html', takes_context=True)
def load_highcharts_js(context):
    values = {}
    return values
