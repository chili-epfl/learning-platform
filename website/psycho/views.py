from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.contrib import messages
import datetime
import website.settings
import random
import pdb;

from psycho.models import User, Test, Question, Activity
from psycho.forms import RegistrationForm, ResponseForm

# Create your views here.

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            test = Test.objects.get(id=1)
            email = form.cleaned_data['email']
            user = User.objects.get(email = email)
            #next_form = ResponseForm(request.POST, test=test, user=user)
            
            return HttpResponseRedirect(reverse('url_quizz', args=(test.id,user.id,)))
    else:
            form = RegistrationForm()

    return render(request, 'psycho/registration.html', {'form':form})

def TestDetail(request,id, user):
    test = Test.objects.get(id=id)
    user = User.objects.get(id=user)
    boolean_val = (request.method == 'POST')
    if boolean_val:
        form = ResponseForm(request.POST, test=test, user=user)
        if form.is_valid():
            response = form.save()
            if test.category == "PSYCHO":
                next_test = Test.objects.get(id=2)
                return HttpResponseRedirect(reverse('url_quizz', args=(next_test.id, user.id,)))
            elif test.category == "PRETEST":
                return HttpResponseRedirect("/psycho/activity/%s" % user.id)

    else:
        form = ResponseForm(test=test, user=user)
        # TODO sort by category, include category?
    return render(request, 'psycho/quiz.html', {'response_form': form, 'test': test, 'user':user})

def AssignActivity(request, user):
    random_idx = random.randint(0, Activity.objects.count() - 1)
    user = User.objects.get(id=user)
    activity = Activity.objects.all()[random_idx]
    if request.method == 'POST':
        if user.activity_one == None:
            user.activity_one = activity.id
        elif user.activity_two == None:
            user.activity_two = activity.id
        user.save()
        return render(request, 'psycho/greetings.html')

    return render(request, 'psycho/activity.html', {'user':user,'activity': activity})

def Confirm(request, uuid):
	email = 'info_chili@epfl.ch'
	return render(request, 'psycho/confirm.html', {'uuid':uuid, 'email': email})