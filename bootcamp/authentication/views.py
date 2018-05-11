from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from bootcamp.authentication.forms import SignUpForm
from bootcamp.feeds.models import Feed
from bootcamp.groups.models import Group,Membership


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            job_title = form.cleaned_data.get('job_title')
            location = form.cleaned_data.get('location')
            new_user = User.objects.create_user(username=username, password=password,
                                     email=email)

            # non-native fields
            new_user.job_title = job_title
            new_user.location  = location

            # create private group
            group = Group.objects.create(group_name="Private",description="{}'s private repository.".format(username),is_private=True)
            group.save()
            
            # force member to join group
            member = Membership.objects.create(user=new_user,group=group,status=3) 
            member.save()         
            
            user = authenticate(username=username, password=password)
            login(request, user)
            welcome_post = '{0} has joined the network.'.format(user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()
            return redirect('/')

    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm()})



