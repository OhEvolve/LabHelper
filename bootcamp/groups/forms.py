from django import forms

from django.utils.safestring import mark_safe
from django.contrib import admin 

#from crispy_forms.helper import FormHelper
#from crispy_forms.bootstrap import InlineRadios

from bootcamp.groups.models import Group,Membership
from bootcamp.authentication.models import User


class HorizontalRadioSelect(forms.RadioSelect):
    temnplate_name = 'horizontal_select.html'

class MembershipForm(forms.ModelForm):

    STATUS = (
    (1, 'Pending'),
    (2, 'Accept'),
    (0, 'Reject'),
    )

    user = forms.CharField(disabled=True)
    status = forms.ChoiceField(choices=STATUS, widget=HorizontalRadioSelect())

    """
    status = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=40)
    """

    class Meta:
        model = Membership
        fields = ('user','status',)



class GroupForm(forms.ModelForm):
    """ Form for creating group """ 
    group_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=2000)

    class Meta:
        model = Group
        exclude = []
        #fields = ['group_name', 'description']

class ManageGroupForm(forms.ModelForm):

    group_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=2000)

    class Meta:
        model = Group 
        fields = ['group_name', 'description']



class JoinRequestForm(forms.ModelForm):

    """ Dynamically generate choices """
    def __init__(self,*args,**kwargs):

        user_groups = kwargs.pop('user_groups')
        super(JoinRequestForm,self).__init__(*args,**kwargs)
        self.fields['group'].choices = user_groups

    """ Form for creating group """ 
    group = forms.ChoiceField(required=False, choices=[])
    '''
    group = forms.ChoiceField(
        choices = Group.objects.none(), # FILTER for non-user groups
        required=True)
    '''

    class Meta:
        model = Membership
        fields = ['group']


        
        
'''
class LeaveGroupForm(forms.ModelForm):
    """ Form for creating group """ 
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True)

    class Meta:
        model = Membership
        fields = ['group']
'''
