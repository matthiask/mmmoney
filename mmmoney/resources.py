from collections import defaultdict
from datetime import date

from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.forms.models import modelform_factory
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from towel import resources
from towel.mt import AccessDecorator
from towel.mt.forms import ModelForm, SearchForm
from towel.resources.mt import MultitenancyMixin
from towel.resources.urls import resource_url_fn

from mmmoney.models import Access, Entry, List


access = AccessDecorator()


class EntrySearchForm(SearchForm):
    pass


class DateInput(forms.DateInput):
    input_type = "date"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if isinstance(value, date):
            context["widget"]["value"] = value.isoformat()
        return context


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = ("client", "created", "currency")
        widgets = {
            "date": DateInput,
            "paid_by": forms.RadioSelect,
            "list": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        if not kwargs.get("instance"):
            request = kwargs.get("request")
            kwargs.setdefault("initial", {}).update({
                "paid_by": request.user.id,
                "date": date.today().isoformat(),
            })

        super().__init__(*args, **kwargs)

        users = (
            User.objects.for_access(self.request.access)
            .filter(is_active=True)
            .order_by("first_name", "last_name")
        )

        self.fields["date"].widget.input_type = "date"
        self.fields["paid_by"].choices = [(u.id, u) for u in users]

        self.fields["list"].choices = [
            (obj.id, obj.name)
            for obj in self.fields["list"].queryset.filter(
                Q(personal=None) | Q(personal=kwargs.get("request").user)
            )
        ]


class EntryMixin(MultitenancyMixin):
    def allow_delete(self, object=None, *, silent=True):
        if object is None:
            return True
        if object.paid_by == self.request.user:
            return True
        if not silent:
            messages.error(
                self.request, _("You are not allowed to delete %s.") % object
            )
        return False

    def get_batch_actions(self):
        return []

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(list__personal=None) | Q(list__personal=self.request.user.id))
        )

    def get_form_class(self):
        """
        Returns the form class used in the view.
        """
        return modelform_factory(
            self.model,
            form=self.form_class,
            fields="__all__",
        )


class EntryFormMixin:
    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            _("The %(verbose_name)s has been successfully saved.")
            % self.object._meta.__dict__,
        )
        return redirect(self.object.urls.url("list"))


class EntryStatsView(resources.ModelResourceView):
    template_name_suffix = "_stats"

    def get(self, request, *args, **kwargs):
        users = list(
            User.objects.filter(access__client=request.access.client_id).order_by(
                "first_name", "username"
            )
        )

        today = date.today()

        until_last_years_end = {
            row["paid_by"]: row["total__sum"]
            for row in (
                Entry.objects.for_access(request.access)
                .order_by()
                .filter(date__year__lt=today.year, list__personal=None)
                .values("paid_by")
                .annotate(Sum("total"))
            )
        }
        this_year = (
            Entry.objects.for_access(request.access)
            .order_by()
            .filter(date__year=today.year)
            .values("paid_by", "list")
            .annotate(Sum("total"))
        )

        stats = defaultdict(lambda: defaultdict(int))
        for row in this_year:
            stats[row["list"]][row["paid_by"]] += row["total__sum"]

        client_table = []
        personal_table = []
        personal_sum = 0

        for obj in List.objects.filter(
            Q(client=request.access.client_id),
            Q(personal=request.user.id) | Q(personal=None),
        ):
            if obj.personal_id:
                personal_table.append([obj, stats[obj.id][obj.personal_id]])
                personal_sum += stats[obj.id][obj.personal_id]

            else:
                paid = stats[obj.id]
                if not len(paid):
                    continue

                client_table.append(
                    [obj]
                    + [paid.get(user.id, 0) for user in users]
                    + [paid.get(request.user.id, 0) - sum(paid.values()) / len(users)]
                )

        until_last_year_sum = [
            until_last_years_end.get(user.id, 0) for user in users
        ] + [
            until_last_years_end.get(request.user.id, 0)
            - sum(until_last_years_end.values()) / len(users)
        ]

        client_sum = [sum(column) for column in list(zip(*client_table))[1:]]

        total_sum = [a + b for a, b in zip(until_last_year_sum, client_sum)]

        return self.render_to_response({
            "users": users,
            "last_year_year": today.year - 1,
            "this_year_year": today.year,
            "until_last_year_sum": until_last_year_sum,
            "client_table": client_table,
            "client_sum": client_sum,
            "total_sum": total_sum,
            "personal_table": personal_table,
            "personal_sum": personal_sum,
            "personal_until_last_year_sum": Entry.objects.for_access(request.access)
            .filter(list__personal=request.user, date__year__lt=today.year)
            .aggregate(Sum("total"))["total__sum"]
            or 0,
            # 'thead': by_set,
            # 'tbody': tbody,
            # 'sumsum': sumsum,
        })


entry_url = resource_url_fn(
    Entry, decorators=(access(Access.MEMBER),), mixins=(EntryMixin,)
)


urlpatterns = [
    entry_url("list", paginate_by=50, search_form=EntrySearchForm, url=r"^$"),
    entry_url("stats", view=EntryStatsView, url=r"^stats/$"),
    entry_url(
        "add", form_class=EntryForm, url=r"^add/$", mixins=(EntryFormMixin, EntryMixin)
    ),
    entry_url("edit", form_class=EntryForm, mixins=(EntryFormMixin, EntryMixin)),
    entry_url("delete"),
]
