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
from django.forms import formset_factory,inlineformset_factory,modelformset_factory

from bootcamp.activities.models import Activity
from bootcamp.decorators import ajax_required
from bootcamp.protocols.forms import CreateProtocolForm,StepForm,BaseStepFormset
from bootcamp.protocols.models import Protocol,Step
from bootcamp.groups.models import Group


@login_required
def protocols(request):
	
    user = request.user
    
    protocols = Protocol.objects.all()
    
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

    StepFormset = formset_factory(StepForm, formset=BaseStepFormset)

    if request.method == 'POST':

        form = CreateProtocolForm(request.POST,**form_vars)
        formset = StepFormset(request.POST)

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
            return render(request, 'protocols/create_protocol.html', {
                'form': form,
                'formset':formset,
            })
        
    else:

        form = CreateProtocolForm(**form_vars)
        #formset = StepFormset()
        formset = modelformset_factory(Step,fields=('name',))

        print(formset)
        print(type(formset))

        return render(request, 'protocols/create_protocol.html', {
            'form': form,
            'formset':formset,
        })















