from collections import OrderedDict, defaultdict

from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncYear
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from towel import resources
from towel.forms import towel_formfield_callback
from towel.mt import AccessDecorator
from towel.mt.forms import SearchForm, ModelForm
from towel.resources.mt import MultitenancyMixin
from towel.resources.urls import resource_url_fn

from mmmoney.models import Access, Entry


access = AccessDecorator()


class EntrySearchForm(SearchForm):
    pass


class EntryForm(ModelForm):
    formfield_callback = towel_formfield_callback

    class Meta:
        model = Entry
        exclude = ('client', 'created', 'currency')
        widgets = {
            'paid_by': forms.RadioSelect,
            'list': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        if not kwargs.get('instance'):
            request = kwargs.get('request')
            kwargs.setdefault('initial', {}).update({
                'paid_by': request.user.id,
            })

        super(EntryForm, self).__init__(*args, **kwargs)

        users = User.objects.for_access(self.request.access).filter(
            is_active=True).order_by('first_name', 'last_name')

        self.fields['paid_by'].choices = [
            (u.id, u) for u in users]

        self.fields['list'].choices = [
            (l.id, l.name) for l in self.fields['list'].queryset.all()]


class EntryMixin(object):
    def allow_delete(self, object=None, silent=True):
        if object is None:
            return True
        if object.paid_by == self.request.user:
            return True
        if not silent:
            messages.error(self.request, _(
                'You are not allowed to delete %s.') % object)
        return False

    def get_batch_actions(self):
        return []


class EntryFormMixin(object):
    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            _('The %(verbose_name)s has been successfully saved.') %
            self.object._meta.__dict__,
        )
        return redirect(self.object.urls.url('list'))


class EntryStatsView(resources.ModelResourceView):
    template_name_suffix = '_stats'

    def get(self, request, *args, **kwargs):
        by_set = set()
        by_dict = dict((u.id, u) for u in User.objects.filter(
            access__client=request.access.client_id,
        ))

        queryset = Entry.objects.for_access(
            request.access
        ).order_by().annotate(
            date_year=TruncYear('date'),
        ).values(
            'paid_by',
            'date_year',
        ).annotate(
            total=Sum('total'),
        )

        stats = defaultdict(lambda: defaultdict(int))
        for row in queryset:
            stats[row['date_year']][by_dict[row['paid_by']]] += row['total']
            by_set.add(by_dict[row['paid_by']])

        by_set = sorted(
            by_set,
            key=lambda user: (user.first_name, user.username))

        sumsum = OrderedDict.fromkeys(by_set, 0)

        tbody = []
        for year, year_data in sorted(stats.items(), reverse=True):
            row = [year, [], 0]
            for by_instance in by_set:
                row[1].append(year_data.get(by_instance, 0))
                sumsum[by_instance] += year_data.get(by_instance, 0)
            row[2] = sum(row[1], 0)
            tbody.append(row)

        return self.render_to_response({
            'thead': by_set,
            'tbody': tbody,
            'sumsum': sumsum,
        })


entry_url = resource_url_fn(
    Entry,
    decorators=(access(Access.MEMBER,),),
    mixins=(EntryMixin, MultitenancyMixin),
)


urlpatterns = [
    entry_url(
        'list',
        paginate_by=50,
        search_form=EntrySearchForm,
        url=r'^$',
    ),
    entry_url(
        'stats',
        view=EntryStatsView,
        url=r'^stats/$',
    ),
    entry_url(
        'add',
        form_class=EntryForm,
        url=r'^add/$',
        mixins=(EntryFormMixin, EntryMixin, MultitenancyMixin),
    ),
    entry_url(
        'edit',
        form_class=EntryForm,
        mixins=(EntryFormMixin, EntryMixin, MultitenancyMixin),
    ),
    entry_url(
        'delete',
    ),
]
