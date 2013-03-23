from django.contrib import admin

from mmmoney import models


class AccessInline(admin.TabularInline):
    model = models.Access
    extra = 1


admin.site.register(models.Client,
    inlines=[AccessInline],
    )
admin.site.register(models.List,
    list_display=('__unicode__', 'name', 'ordering', 'client'),
    list_editable=('name', 'ordering'),
    list_filter=('client',),
    )
admin.site.register(models.Entry,
    date_hierarchy='date',
    list_display=('date', 'paid_by', 'list', 'total', 'notes', 'client'),
    list_filter=('paid_by', 'list', 'client'),
    search_fields=models.Entry.objects.search_fields,
    )
