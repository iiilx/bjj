from django.forms import ModelForm
from django.forms.formsets import BaseFormSet, formset_factory
from bjj.poll.models import *

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ('choice',)

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ('question',)
ChoiceFormSet = formset_factory(ChoiceForm, extra=5, max_num=5, formset=RequiredFormSet)

