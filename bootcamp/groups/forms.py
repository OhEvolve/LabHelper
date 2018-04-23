from django import forms

from bootcamp.groups.models import Group


class GroupForm(forms.ModelForm):
    group_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=2000)

    class Meta:
        model = Group
        fields = ['group_name', 'description', 'tags']
