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
from bootcamp.groups.forms import GroupForm,JoinRequestForm,ManageGroupForm,MembershipForm
from bootcamp.groups.models import Group,Membership

# Create your views here.
class ReagentsOverview(ListView):
    template_name = 'reagents/reagents.html'
    context_object_name = 'reagents'

    def get_queryset(self):
        return Liquid.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(ReagentsOverview, self).get_context_data(**kwargs)
        context['reagent_count'] = sum([obj.objects.count() for obj in (Liquid,Solid,Biologic,Solution)])
        # add reagent references (probably not necessary, just need counts)
        context['liquids'] = Liquid.objects.all()
        context['solids'] = Solid.objects.all()
        context['biologics'] = Biologic.objects.all()
        context['solutions'] = Solution.objects.all()
        # return modified context
        return context
        
@login_required
def reagents(request):
	
    users_list = User.objects.filter(is_active=True).order_by('username')
    groups_list = Group.objects.order_by('group_name')
    user = request.user

    
    return render(request, 'reagents/reagents.html', {'groups': groups_list,
                                                  'user':   user,
                                                  'admin_groups': [m.group for m in user.membership_set.all() if m.status == 3]})
