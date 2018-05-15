
from django import forms

from bootcamp.groups.models import Group
from bootcamp.reagents.models import Liquid,Solid,Biologic,Solution,Cell


class CreateReagentForm(forms.ModelForm):

    """ Base reagent form class """

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
        model = Liquid 
        fields = ['name', 'groups']

class CreateSolidForm(CreateReagentForm):

    class Meta:
        model = Solid 
        fields = ['name', 'groups','mw','mw_units']

class CreateBiologicForm(CreateReagentForm):

    class Meta:
        model = Biologic 
        fields = ['name', 'groups','sequence','form','shape','material']

class CreateBiologicForm(CreateReagentForm):

    class Meta:
        model = Biologic 
        fields = ['name', 'groups','sequence','form','shape','material']

class CreateSolutionForm(CreateReagentForm):

    class Meta:
        model = Solution
        #model = Solution.liquids.through
        #inlines = (
        #fields = ['name']
        fields = ['name', 'groups','liquids','solids','biologics']

class CreateCellForm(CreateReagentForm):

    class Meta:
        model = Cell 
        fields = ['name', 'groups','species','morphology','shaken','media_preference','doubling_time','doubling_time_units','culture_environment']







