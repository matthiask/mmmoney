from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from towel.managers import SearchManager


class List(models.Model):
    name = models.CharField(_('name'), max_length=100)
    ordering = models.IntegerField(_('ordering'), default=0)

    class Meta:
        ordering = ['ordering']
        verbose_name = _('list')
        verbose_name_plural = _('lists')

    def __unicode__(self):
        return self.name


class EntryManager(SearchManager):
    search_fields = ('list__name', 'paid_by__first_name', 'paid_by__last_name',
        'currency', 'total', 'notes')


class Entry(models.Model):
    CURRENCY_CHOICES = (
        ('CHF', 'CHF'),
        )

    created = models.DateTimeField(_('created'), default=datetime.now)
    date = models.DateField(_('date'), default=date.today)

    paid_by = models.ForeignKey(User, verbose_name=_('paid by'),
        related_name='entries')
    list = models.ForeignKey(List, verbose_name=_('list'),
        related_name='entries')
    currency = models.CharField(_('currency'), max_length=3,
        choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0][0])
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2)
    notes = models.TextField(_('notes'), blank=True)

    objects = EntryManager()

    class Meta:
        ordering = ['-date', '-created']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    @models.permalink
    def get_absolute_url(self):
        return ('mmmoney_entry_edit', (), {'pk': self.pk})
