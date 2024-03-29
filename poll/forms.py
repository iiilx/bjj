from django.forms import ModelForm
from django.forms.formsets import BaseFormSet, formset_factory 
from bjj.poll.models import *
from django.forms.models import inlineformset_factory

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

#ChoiceFormSet = inlineformset_factory(Poll, Choice, extra=5)
ChoiceFormSet = formset_factory(ChoiceForm, extra=2, max_num=5, formset=RequiredFormSet)

