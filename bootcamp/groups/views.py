from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.forms import formset_factory,inlineformset_factory

from bootcamp.activities.models import Activity
from bootcamp.decorators import ajax_required
from bootcamp.groups.forms import GroupForm,JoinRequestForm,ManageGroupForm,MembershipForm
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

    if request.method == 'POST':

        form = GroupForm(request.POST)

        if form.is_valid():
            group_name = form.cleaned_data.get('group_name')
            description = form.cleaned_data.get('description')
            user = request.user
            
            group = Group.objects.create(group_name=group_name,description=description)
            group.save()
            
            member = Membership.objects.create(user=user,group=group,status=3) 
            member.save()         
            
            messages.add_message(request,
                    messages.SUCCESS,
                    'Group created!')

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

        form = GroupForm()
        return render(request, 'groups/create_group.html',
                      {'form': form})


@login_required
def join_request(request):
	 
    if request.method == 'POST':

        form = JoinRequestForm(request.POST)

        if form.is_valid():
            group = form.cleaned_data.get('group')
            user = request.user
            status = 1
            
            membership = Membership.objects.create(user=user,group=group,status=status)
            membership.save()


            messages.add_message(request,
                    messages.SUCCESS,
                    'Request sent!')
            
            return redirect('/groups')
            
        else:
            group_name = form.cleaned_data.get('group')
            return render(request, 'groups/join_request.html', {
                'group': group,
                'form': form
            })

        
    else:
        
        form = JoinRequestForm()
        return render(request, 'groups/join_request.html',
                      {'form': form})


# TODO: require admin privileges
@login_required
def manage_group(request,group_id):

    group = Group.objects.get(pk=group_id)
    user = request.user
    memberships = Membership.objects.filter(group=group).order_by('status')

    if request.method == 'POST':
        form = ManageGroupForm(request.POST)
        formset = inlineformset_factory(Group,Membership,fields=('status',)) 

        if form.is_valid():
            group.group_name = form.cleaned_data.get('group_name')
            group.description = form.cleaned_data.get('description')
            print('Get data:',form.cleaned_data.get('id_Taeyoon'))
            
            group.save()
            
            messages.add_message(request,
                    messages.SUCCESS,
                    'Group properties saved!')

            return redirect('/groups')
            
    else:
        form = ManageGroupForm(instance=user, initial={
            'group_name': group.group_name,
            'description':group.description,
            })
        #MembershipFormSet = inlineformset_factory(MembershipForm,extra=0)
        MembershipFormSet = inlineformset_factory(Group,Membership,fields=('status',)) 
        formset = MembershipFormSet(initial=[{
            'user':membership.user,
            'status':membership.status}
            for membership in memberships])

    return render(request, 'groups/manage_group.html', {
        'form': form,
        'formset': formset,
        'group_name':group.group_name,
        'group_id':group_id
        })

        
@login_required
@ajax_required
def leave_group(request):
    membership_id = request.POST['membership']
    membership = Membership.objects.get(pk=membership_id)

    user = request.user

    if True:#membership.group.user == user: # TODO: create check for admin level permission
        membership.delete()
        return HttpResponseRedirect(reverse('groups'))

    else:
        return HttpResponseForbidden()

@login_required
@ajax_required
def delete_group(request):
    raise NotImplementedError    

@login_required
@ajax_required
def transfer_admin(request):
    raise NotImplementedError    





        
        
        




















