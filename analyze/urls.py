from django.conf.urls import url
from . import views

app_name = 'analyze'

urlpatterns = [
    url(r'^works/$', views.WorkAnalyze.as_view(), name='works_analyze'),
]
