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
from bootcamp.reagents.models import Liquid,Solid,Biologic,Solution,Cell,Ownership
from bootcamp.groups.models import Group


@login_required
def reagents(request):
	
    user = request.user
    
    liquids   = Liquid.objects.all()
    solids    = Solid.objects.all()
    biologics = Biologic.objects.all()
    solutions = Solution.objects.all()
    cells     = Cell.objects.all()
    
    return render(request, 'reagents/reagents.html', {
        'liquids':   liquids,
        'solids':    solids,
        'biologics': biologics,
        'solutions': solutions,
        'cells':     cells,
        })


@login_required
def create_liquid(request):
    kwargs = {
            'tag':'liquid',
            'form':CreateLiquidForm,
            'form_vars':{},
            'model':Liquid,
            'model_vars':[],
            }
    return create_reagent(request,**kwargs)

@login_required
def create_solid(request):
    kwargs = {
            'tag':'solid',
            'form':CreateSolidForm,
            'form_vars':{},
            'model':Solid,
            'model_vars':['mw','mw_units'],
            }
    return create_reagent(request,**kwargs)

@login_required
def create_biologic(request):
    kwargs = {
            'tag':'biologic',
            'form':CreateBiologicForm,
            'form_vars':{},
            'model':Biologic,
            'model_vars':['sequence','form','shape','material'],
            }
    return create_reagent(request,**kwargs)

@login_required
def create_solution(request):
    kwargs = {
            'tag':'solution',
            'form':CreateSolutionForm,
            'form_vars':{},
            'model':Solution,
            'model_vars':['liquidcontent','solids','biologics'],
            }
    return create_reagent(request,**kwargs)

@login_required
def create_cell(request):
    kwargs = {
            'tag':'cell',
            'form':CreateCellForm,
            'form_vars':{},
            'model':Cell,
            'model_vars':['species','morphology','shaken','media_preference','doubling_time','doubling_time_units','culture_environment'],
            }
    return create_reagent(request,**kwargs)

# Needed variables:
# - tag 
# - form
# - form_vars
# - model (model)
# - model_vars (tuple of strings)


@login_required
def create_reagent(request,**settings):

    user = request.user

    # change to accepted groups
    default_form_vars = {
            'user_groups': Group.objects.filter(membership__user__username=user.username),
            }
    form_vars = settings['form_vars']
    form_vars.update(default_form_vars)

    if request.method == 'POST':

        form = settings['form'](request.POST,**form_vars)

        if form.is_valid():

            default_model_parameters = {'name':form.cleaned_data.get('name')}
            model_parameters = dict([(s,form.cleaned_data.get(s)) 
                                     for s in settings['model_vars']])
            model_parameters.update(default_model_parameters)
            
            reagent = settings['model'].objects.create(**model_parameters)

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


















