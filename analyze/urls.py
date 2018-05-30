from django.conf.urls import url
from . import views

app_name = 'analyze'

urlpatterns = [
    url(r'^works/$', views.WorkAnalyze.as_view(), name='works_analyze'),
    url(r'^data/$', views.get_datatables_data, name='get_data'),
    url(r'^works/sample/(?P<pk>[0-9]+)$', views.SelectedSample.as_view(),
        name='work_sample'),
]
