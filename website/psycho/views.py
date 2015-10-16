from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
import website.settings
import pdb;

from psycho.models import User, Test, Question
from psycho.forms import RegistrationForm, ResponseForm

# Create your views here.

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'psycho/greetings.html')
    else:
            form = RegistrationForm()

    return render(request, 'psycho/registration.html', {'form':form})

def TestDetail(request,id):
    test = Test.objects.get(id=id)
    boolean_val = (request.method == 'POST')
    if boolean_val:
        form = ResponseForm(request.POST, test=test)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
            '''return render(request,'psycho/greetings.html')'''
    else:
        form = ResponseForm(test=test)
        # TODO sort by category, include category?
    return render(request, 'psycho/quiz.html', {'response_form': form, 'test': test})

def Confirm(request, uuid):
	email = settings.support_email
	return render(request, 'psycho/confirm.html', {'uuid':uuid, 'email': email})