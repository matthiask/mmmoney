from datetime import date, datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from towel.managers import SearchManager
from towel.resources.urls import model_resource_urls


@model_resource_urls()
class Client(models.Model):
    name = models.CharField(_("client"), max_length=100)

    class Meta:
        verbose_name = _("client")
        verbose_name_plural = _("clients")

    def __str__(self):
        return self.name


@model_resource_urls()
class Access(models.Model):
    MEMBER = access = 10

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_("client")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))

    class Meta:
        verbose_name = _("access")
        verbose_name_plural = _("accesses")


class ListManager(SearchManager):
    search_fields = ("name",)

    def for_access(self, access):
        return self.filter(client=access.client_id)


@model_resource_urls()
class List(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_("client")
    )
    name = models.CharField(_("name"), max_length=100)
    ordering = models.IntegerField(_("ordering"), default=0)
    personal = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("personal list"),
        blank=True,
        null=True,
    )

    objects = ListManager()

    class Meta:
        ordering = ["ordering"]
        verbose_name = _("list")
        verbose_name_plural = _("lists")

    def __str__(self):
        return self.name

    def clean(self):
        if self.personal and self.personal.access.client != self.client:
            raise ValidationError(
                _("Personal list client does not match with list client.")
            )


class EntryManager(SearchManager):
    search_fields = (
        "list__name",
        "paid_by__first_name",
        "paid_by__last_name",
        "currency",
        "total",
        "notes",
    )

    def for_access(self, access):
        return self.filter(client=access.client_id)


@model_resource_urls(default="edit")
class Entry(models.Model):
    CURRENCY_CHOICES = (("CHF", "CHF"),)

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_("client")
    )

    created = models.DateTimeField(_("created"), default=datetime.now)
    date = models.DateField(_("date"), default=date.today)

    paid_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("paid by"),
        related_name="entries",
    )
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, verbose_name=_("list"), related_name="entries"
    )
    currency = models.CharField(
        _("currency"),
        max_length=3,
        choices=CURRENCY_CHOICES,
        default=CURRENCY_CHOICES[0][0],
    )
    total = models.DecimalField(_("total"), max_digits=10, decimal_places=2)
    notes = models.CharField(_("notes"), max_length=200)

    objects = EntryManager()

    class Meta:
        ordering = ["-date", "-created"]
        verbose_name = _("entry")
        verbose_name_plural = _("entries")

    def __str__(self):
        return self.notes


class UserManagerMixin:
    def for_access(self, access):
        return self.filter(access__client=access.client_id)


User.objects.__class__.__bases__ += (UserManagerMixin,)
User.__str__ = lambda self: self.get_full_name() or self.username
