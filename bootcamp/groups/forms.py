from django import forms

from bootcamp.groups.models import Group,Membership


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
        fields = ['group_name', 'description', 'tags']


class JoinRequestForm(forms.ModelForm):
    """ Form for creating group """ 
    group = forms.ModelChoiceField(
        queryset = Group.objects.all(), # FILTER for non-user groups
        required=True)

    class Meta:
        model = Membership
        fields = ['group']
        
        
class LeaveGroupForm(forms.ModelForm):
    """ Form for creating group """ 
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True)

    class Meta:
        model = Membership
        fields = ['group']
