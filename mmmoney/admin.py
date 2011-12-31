from django.contrib import admin

from mmmoney import models


admin.site.register(models.List,
    list_display=('__unicode__', 'name', 'ordering'),
    list_editable=('name', 'ordering'),
    )
admin.site.register(models.Entry,
    date_hierarchy='date',
    list_display=('date', 'paid_by', 'list', 'total', 'notes'),
    list_filter=('paid_by', 'list'),
    search_fields=models.Entry.objects.search_fields,
    )
