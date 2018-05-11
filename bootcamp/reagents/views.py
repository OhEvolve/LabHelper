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
from bootcamp.reagents.forms import CreateLiquidForm
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

    user = request.user
    # change to accepted groups
    user_groups = Group.objects.filter(membership__user__username=user.username)

    if request.method == 'POST':

        # Needed variables
        # - form
        # - form variable dictionary
        # - model
        # - model strings
        


        form = CreateLiquidForm(request.POST,user_groups=user_groups)

        if form.is_valid():

            default_parameters = {
                    'name':form.cleaned_data.get('name'),
                    }


           
            liquid = Liquid.objects.create()
            #liquid = Liquid.objects.create(
            #        name=name,
            #        )
            liquid.name = form.cleaned_data.get('name')
            liquid.save()

            groups = form.cleaned_data.get('groups')
            ownership = Ownership.objects.create(group=groups,matter=liquid) 
            ownership.save()         
            
            messages.add_message(request,
                    messages.SUCCESS,
                    'New liquid added!')

            return redirect('/reagents')
            
        else:
            return render(request, 'reagents/create_reagent.html', {
                'form': form,
                'url_label': 'create_liquid',
                'page_label': 'Create Liquid',
            })
        
    else:

        form = CreateLiquidForm(user_groups=user_groups)
        return render(request, 'reagents/create_reagent.html', {
            'form': form,
            'type': 'liquid',
            'url_label': 'create_liquid',
            'page_label': 'Create Liquid',
            })


















