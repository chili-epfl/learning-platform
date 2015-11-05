from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.contrib import messages
import datetime
from django.utils import timezone
import website.settings
import random
import pdb;

from psycho.models import User, Test, Question, Activity, UserActivity
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

#We can also assume that there is always an even number of activities by category
def AssignActivity(request, user):
    
    user = User.objects.get(id=user)
    
    total_items = Activity.objects.filter(category=Activity.CONCEPT_1).count()
    random_idx = random.randint(0, total_items - 1)
    offset=0
    if UserActivity.objects.filter(user=user).exists():
        offset=Activity.CONCEPT_1
        #offset=2*Activity.CONCEPT_1 set to 1 for now to test
    activity = Activity.objects.all()[offset+random_idx]
    
    if request.method == 'POST':
        user_activity = UserActivity(user=user,activity=activity)
        user_activity.save()
        if UserActivity.objects.filter(user=user).count()<2:
            return HttpResponseRedirect("/psycho/activity/%s" % user.id)
        else:
            return HttpResponseRedirect(reverse('url_greetings'))
        #return render(request, 'psycho/greetings.html')

    return render(request, 'psycho/activity.html', {'user':user,'activity': activity})

