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
import pdb
import hashlib

from psycho.models import User, Test, Question, Activity, UserActivity, Response
from psycho.forms import RegistrationForm, ResponseForm


'''view for registration form'''
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            test = Test.objects.get(category="PSYCHO")
            email = form.cleaned_data['email']
            user = User.objects.get(email = email)
            #next_form = ResponseForm(request.POST, test=test, user=user)
            
            return HttpResponseRedirect(reverse('url_quizz', args=(test.id,user.id,)))
    else:
            form = RegistrationForm()

    return render(request, 'psycho/registration.html', {'form':form})

#This function is used for Psycholgical test, pre-test and post-test
def TestDetail(request,id, user):
    test = Test.objects.get(id=id)
    user = User.objects.get(id=user)
    if request.method == 'POST':
        form = ResponseForm(request.POST, test=test, user=user)
        if form.is_valid():
            response = form.save()
            if test.category == "PSYCHO":
                #for now there is only one pre-test, add the selection if more
                next_test = Test.objects.get(category="PRETEST")
                return HttpResponseRedirect(reverse('url_quizz', args=(next_test.id, user.id,)))
            elif test.category == "PRETEST":
                if Response.objects.filter(user=user,test=test).count()<2:
                    return HttpResponseRedirect(reverse('url_intro', args=(user.id,)))
                else:
                    next_test = Test.objects.get(category="ASSESS")
                    return HttpResponseRedirect(reverse('url_quizz', args=(next_test.id, user.id,)))    
            elif test.category =="ASSESS":
                return HttpResponseRedirect(reverse('url_greetings'))
    else:
        form = ResponseForm(test=test, user=user)
    return render(request, 'psycho/quiz.html', {'response_form': form, 'test': test, 'user':user})

#We assume there is always an even number of activities by category
def AssignActivity(request, user):
    
    user = User.objects.get(id=user)
    '''determine a random path for the activities based on a unique generated number'''
    unique = request.session.session_key+user.email
    unique = hashlib.sha224(unique).hexdigest()
    last=unique[len(unique)-1]
    last="{:08b}".format(int(last,16))
    a1_id = last[6]
    a2_id = last[7]
    #total_items = Activity.objects.filter(category=Activity.CONCEPT_1).count()
    #random_idx = random.randint(0, total_items - 1)
    '''The offset is used to select an activity from the following concept'''
    offset=0
    if UserActivity.objects.filter(user=user).exists():
        activity = Activity.objects.order_by('category')[2+int(a2_id)]
    else:
        activity = Activity.objects.order_by('category')[int(a1_id)]
    
    if request.method == 'POST':
        user_activity = UserActivity(user=user,activity=activity)
        user_activity.save()
        if UserActivity.objects.filter(user=user).count()<2:
            return HttpResponseRedirect("/activity/%s" % user)
        else:
            test=Test.objects.get(category="PRETEST")
            return HttpResponseRedirect(reverse('url_quizz', args=(test.id,user.id,)))

    return render(request, 'psycho/activity.html', {'user':user,'activity': activity})

def ActivityIntro(request, user):
    if request.method == 'POST':
        return HttpResponseRedirect("/activity/%s" % user)
    
    return render(request, 'psycho/intro.html', {'user':user})


def error404(request):
    return render(request,'404.html')
