from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from towel.forms import towel_formfield_callback
from towel.mt import AccessDecorator
from towel.mt.forms import SearchForm, ModelForm
from towel.mt.modelview import ModelView

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
        super(EntryForm, self).__init__(*args, **kwargs)

        users = User.objects.for_access(self.request.access).filter(
            is_active=True).order_by('first_name', 'last_name')

        self.fields['paid_by'].choices = [
            (u.id, u.get_full_name() or u.username) for u in users]

        self.fields['list'].choices = [
            (l.id, l.name) for l in self.fields['list'].queryset.all()]


class EntryModelView(ModelView):
    paginate_by = 50
    search_form = EntrySearchForm

    def view_decorator(self, func):
        return access(Access.MEMBER)(func)

    def crud_view_decorator(self, func):
        return access(Access.MEMBER)(func)

    def additional_urls(self):
        return [
            (r'^stats/$', self.view_decorator(self.stats)),
        ]

    def get_form_instance(
            self, request, form_class, instance=None, change=None, **kwargs):
        args = self.extend_args_if_post(request, [])
        kwargs['instance'] = instance
        kwargs['request'] = request
        if not change:
            kwargs['initial'] = {
                'paid_by': request.user.id,
            }
        return EntryForm(*args, **kwargs)

    def response_add(self, request, instance, form, formsets):
        messages.success(
            request, _('The new object has been successfully created.'))
        return redirect('mmmoney_entry_list')

    def response_edit(self, request, instance, form, formsets):
        messages.success(
            request, _('The object has been successfully updated.'))
        return redirect('mmmoney_entry_list')

    def deletion_allowed(self, request, instance):
        return request.user == instance.paid_by

    def stats(self, request):
        # TODO handle currency, not necessary yet
        queryset = Entry.objects.for_access(
            request.access
        ).order_by().values('paid_by', 'date').annotate(Sum('total'))
        stats = {}
        users = set()
        user_dict = dict((u.id, u) for u in User.objects.filter(
            access__client=request.access.client_id,
        ))

        for row in queryset:
            month = row['date'].replace(day=1)
            by_month = stats.setdefault(month, {})
            user = user_dict[row['paid_by']]
            users.add(user)

            by_month.setdefault(user, 0)
            by_month[user] += row['total__sum']

        users = sorted(
            users,
            key=lambda user: (user.first_name, user.username))
        tbody = []
        for month, month_data in sorted(stats.items()):
            row = [month, [], 0]
            for user in users:
                row[1].append(month_data.get(user, 0))
            row[2] = sum(row[1], 0)
            tbody.append(row)

        tfoot = [sum(user) for user in zip(*[row[1] for row in tbody])]
        tfoot.append(sum(tfoot, 0))

        return self.render(
            request,
            self.get_template(request, 'stats'),
            self.get_context(request, {
                'thead': users,
                'tbody': tbody,
                'tfoot': tfoot,
            })
        )

entry_views = EntryModelView(Entry)
