
from django import forms
from django.forms.formsets import BaseFormSet

from bootcamp.groups.models import Group
from bootcamp.protocols.models import Protocol,Step


class CreateProtocolForm(forms.Form):

    """ Base protocol form class """

    def __init__(self,*args,**kwargs):

        user_groups = kwargs.pop('user_groups')
        super(CreateProtocolForm,self).__init__(*args,**kwargs)

        self.fields['name'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            max_length=255)

        self.fields['groups'] = forms.ModelChoiceField(
            queryset = Group.objects.none(),
            required=True,
            label='Owners')

        self.fields['groups'].queryset = user_groups


class StepForm(forms.Form):

    """ Base protocol form class """

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)


class BaseStepFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return




