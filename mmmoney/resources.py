from django import forms
from django.conf.urls import patterns
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from towel import resources
from towel.forms import towel_formfield_callback
from towel.mt import AccessDecorator
from towel.mt.forms import SearchForm, ModelForm
from towel.resources.mt import MultitenancyMixin
from towel.resources.urls import resource_url_fn

from mmmoney.models import Access, Entry, List


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
        by = request.GET.get('by', 'paid_by')

        if by == 'paid_by':
            by_set = set()
            by_dict = dict((u.id, u) for u in User.objects.filter(
                access__client=request.access.client_id,
            ))
            by_sorting_key = lambda user: (user.first_name, user.username)

        elif by == 'list':
            by_set = set()
            by_dict = dict((l.id, l) for l in List.objects.for_access(
                request.access
            ))
            by_sorting_key = lambda list_: (list_.ordering, list_.name)

        else:
            messages.error(request, _('Invalid request.'))
            return redirect('.')

        queryset = Entry.objects.for_access(
            request.access
        ).order_by().values(by, 'date').annotate(Sum('total'))
        stats = {}

        for row in queryset:
            month = row['date'].replace(day=1)
            by_month = stats.setdefault(month, {})
            by_instance = by_dict[row[by]]
            by_set.add(by_instance)

            by_month.setdefault(by_instance, 0)
            by_month[by_instance] += row['total__sum']

        by_set = sorted(by_set, key=by_sorting_key)
        tbody = []
        for month, month_data in sorted(stats.items()):
            row = [month, [], 0]
            for by_instance in by_set:
                row[1].append(month_data.get(by_instance, 0))
            row[2] = sum(row[1], 0)
            tbody.append(row)

        tfoot = [sum(column) for column in zip(*[row[1] for row in tbody])]
        tfoot.append(sum(tfoot, 0))

        return self.render_to_response({
            'thead': by_set,
            'tbody': tbody,
            'tfoot': tfoot,
            'by': by,
        })


entry_url = resource_url_fn(
    Entry,
    decorators=(access(Access.MEMBER,),),
    mixins=(EntryMixin, MultitenancyMixin),
)


urlpatterns = patterns(
    '',
    entry_url(
        'list',
        paginate_by=25,
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
)
