from django import forms
from django.contrib.auth.decorators import login_required

from towel import forms as towel_forms, modelview

from mmmoney.models import Entry, List


class EntrySearchForm(towel_forms.SearchForm):
    pass


class EntryForm(forms.ModelForm):
    formfield_callback = towel_forms.stripped_formfield_callback

    class Meta:
        model = Entry
        exclude = ('created', 'currency')


class EntryModelView(modelview.ModelView):
    paginate_by = 50
    search_form = EntrySearchForm

    def view_decorator(self, func):
        return login_required(func)

    def crud_view_decorator(self, func):
        return login_required(func)

    def get_form_instance(self, request, form_class, instance=None, change=None, **kwargs):
        args = self.extend_args_if_post(request, [])
        kwargs['instance'] = instance
        if not change:
            kwargs['initial'] = {
                'paid_by': request.user.id,
                }
        return EntryForm(*args, **kwargs)


entry_views = EntryModelView(Entry)

