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

















