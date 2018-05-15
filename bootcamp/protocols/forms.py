
from django import forms

from bootcamp.groups.models import Group


class CreateProtocolForm(forms.ModelForm):

    """ Base protocol form class """

    def __init__(self,*args,**kwargs):

        user_groups = kwargs.pop('user_groups')
        super(CreateReagentForm,self).__init__(*args,**kwargs)
        self.fields['groups'].queryset = user_groups

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)

    groups = forms.ModelChoiceField(
        queryset = Group.objects.none(),
        required=True,
        label='Owners')

class CreateLiquidForm(CreateReagentForm):
    class Meta:
        model = Protocol  
        fields = ['name', 'groups']








