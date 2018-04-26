from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from bootcamp.activities.models import Activity
from bootcamp.decorators import ajax_required
from bootcamp.groups.forms import GroupForm,JoinGroupForm
from bootcamp.groups.models import Group,Membership

@login_required
def groups(request):
	
    users_list = User.objects.filter(is_active=True).order_by('username')
    groups_list = Group.objects.order_by('group_name')
    user = request.user
    
    return render(request, 'groups/groups.html', {'groups': groups_list,
                                                  'user':   user})


@login_required
def create_group(request):
	 
    form = GroupForm(request.POST)
	 
    if request.method == 'POST':
        if form.is_valid():
            group_name = form.cleaned_data.get('group_name')
            description = form.cleaned_data.get('description')
            user = request.user
            
            group = Group.objects.create(group_name=group_name,description=description)
            group.save()
            
            member = Membership.objects.create(user=user,group=group,status=3) # make creator admin
            member.save()         
            
            # non-native fields
            #new_user.job_title = job_title
            #new_user.location  = location
            
            return redirect('/groups')
            
        else:
            group_name = form.cleaned_data.get('group_name')
            description = form.cleaned_data.get('description')
            return render(request, 'groups/create_group.html', {
                'group_name': group_name,
                'description':description,
                'form': form
            })

        
    else:
        
        return render(request, 'groups/create_group.html',
                      {'form': form})

# UNUSED
class CreateGroup(LoginRequiredMixin, CreateView):
    """
    """
    template_name = 'groups/create_group.html'
    form_class = GroupForm
    success_url = reverse_lazy('create_group')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateGroup, self).form_valid(form)


# PLACEHOLDER FUNCTION

@login_required
def join_group(request):
	 
    form = JoinGroupForm(request.POST)
	 
    if request.method == 'POST':
        if form.is_valid():
            group = form.cleaned_data.get('group')
            user = request.user
            status = 2
            
            membership = Membership.objects.create(user=user,group=group,status=status)
            membership.save()
            
            return redirect('/groups')
            
        else:
            group_name = form.cleaned_data.get('group')
            return render(request, 'groups/join_group.html', {
                'group': group,
                'form': form
            })

        
    else:
        
        return render(request, 'groups/join_group.html',
                      {'form': form})
        
        
        
        
        
        
        

