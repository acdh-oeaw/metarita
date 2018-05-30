To bootstrap the creation of a configuration file for charts:
Start a django-shell session

> python manage.py shell_plus --settings=ecce.settings.postgres

and execute the following

```
from browsing.filters import TokenListFilter
from charts import chart_conf_creator
load_charts = chart_conf_creator.ChartConfigurator(TokenListFilter)
```

This will create a file `charts\chart_config.py`. You can define the filename by adding a parameter to create() like, e.g.

> load_charts.create("whateverYouLike.py")

Now run `load_charts.store_config()` to create database entries form the config file created before.
