from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView,CreateView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.forms import formset_factory,inlineformset_factory

from bootcamp.activities.models import Activity
from bootcamp.decorators import ajax_required
from bootcamp.reagents.forms import CreateLiquidForm,CreateSolidForm,CreateBiologicForm,CreateSolutionForm,CreateCellForm
from bootcamp.protocols.models import Protocol
from bootcamp.groups.models import Group


@login_required
def protocols(request):
	
    user = request.user
    
    print('HERERE')
    protocols = Protocol.objects.all()
    
    print('PROTOCOLS:',protocols)
    
    return render(request, 'protocols/protocols.html', {
        'protocols': protocols,
        })


@login_required
def create_protocol(request,**settings):

    user = request.user

    # change to accepted groups
    form_vars = {
            'user_groups': Group.objects.filter(membership__user__username=user.username),
            }

    if request.method == 'POST':

        form = CreateProtocolForm(request.POST,**form_vars)

        if form.is_valid():

            reagent = Protocol.objects.create()

            reagent.name = form.cleaned_data.get('name')
            reagent.creator = request.user
            reagent.save()

            groups = form.cleaned_data.get('groups')
            ownership = Ownership.objects.create(group=groups,matter=reagent) 
            ownership.save()         
            
            messages.add_message(request,messages.SUCCESS,
                    'New {} added!'.format(settings['tag'])) 

            return redirect('/reagents')
            
        else:
            return render(request, 'reagents/create_reagent.html', {
                'form': form,
                'type': settings['tag'],
                'url_label': 'create_{}'.format(settings['tag']),
                'page_label': 'Create {}'.format(settings['tag'].capitalize()),
            })
        
    else:

        form = settings['form'](**form_vars)
        return render(request, 'reagents/create_reagent.html', {
            'form': form,
            'type': settings['tag'],
            'url_label': 'create_{}'.format(settings['tag']),
            'page_label': 'Create {}'.format(settings['tag'].capitalize()),
        })















