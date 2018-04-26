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
from bootcamp.groups.forms import GroupForm
from bootcamp.groups.models import Group

@login_required
def groups(request):
    users_list = User.objects.filter(is_active=True).order_by('username')
    groups_list = Group.objects.order_by('group_name')
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)

    except PageNotAnInteger:
        users = paginator.page(1)

    except EmptyPage:  # pragma: no cover
        users = paginator.page(paginator.num_pages)

    return render(request, 'groups/groups.html', {'groups':groups_list})


@login_required
def create_group(request):
	 
    form = GroupForm(request.POST)
	 
    if request.method == 'POST':
        if form.is_valid():
            group_name = form.cleaned_data.get('group_name')
            description = form.cleaned_data.get('description')
            
            new_group = Group.objects.create(group_name=group_name,description=description)
            new_group.save()
            
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
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            answer = Answer()
            answer.user = request.user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            user.profile.notify_answered(answer.question)
            return redirect('/questions/{0}/'.format(answer.question.pk))

        else:
            question = form.cleaned_data.get('question')
            return render(request, 'questions/question.html', {
                'question': question,
                'form': form
            })

    else:
        return redirect('/questions/')
        
        
        
        
        
        
        

