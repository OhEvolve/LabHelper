from django import forms

from django.utils.safestring import mark_safe
from django.contrib import admin 

from bootcamp.groups.models import Group,Membership
from bootcamp.authentication.models import User




class MembershipForm(forms.ModelForm):

    STATUS = (
    (0, 'Requested'),
    (1, 'Unsubscribed'),
    (2, 'Joined'),
    (3, 'Admin'),
    )

    user = forms.CharField(disabled=True)
    status = forms.ChoiceField(choices=STATUS, widget=forms.RadioSelect(attrs={
                'display': 'inline-block'
                    }))

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
    """ Form for creating group """ 
    group = forms.ModelChoiceField(
        queryset = Group.objects.all(), # FILTER for non-user groups
        required=True)

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
