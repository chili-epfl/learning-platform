from django import forms
from django.utils.safestring import mark_safe
from django.forms import models
from psycho.models import Question, Test, Response, AnswerText, AnswerRadio, User
import uuid


class RegistrationForm(forms.ModelForm):
    '''Form for the resgitration of the user'''
    class Meta:
        model = User
        exclude = ('score_test', 'score_pre', 'score_post','activity_one','activity_two')

'''horizontal display of the radio buttons'''
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class ResponseForm(models.ModelForm):
    '''Form for the tests 
        The fields are the questions having the test as foreign key and the text of the question is their label'''
    class Meta:
        model = Response
        exclude = ('test','timestamp', 'user')

    def __init__(self, *args, **kwargs):
        # expects a survey object to be passed in initially
        test = kwargs.pop('test')
        user = kwargs.pop('user')
        self.test = test
        self.user = user
        super(ResponseForm, self).__init__(*args, **kwargs)
        
        # add a field for each test question, corresponding to the question
        # type as appropriate.
        data = kwargs.get('data')
        for q in test.questions():
            if q.question_type == Question.TEXT:
                self.fields["question_%d" % q.pk] = forms.CharField(label=q.text,widget=forms.Textarea)
            elif q.question_type == Question.RADIO:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),choices = question_choices)
    
        # initialize the form field with values from a POST request, if any.
            if data:
                    self.fields["question_%d" % q.pk].initial = data.get('question_%d' % q.pk)

    def save(self, commit=True):
        # save the response object
        response = super(ResponseForm, self).save(commit=False)
        response.test = self.test
        response.user = self.user
        #add user column
        response.save()
        # create an answer object for each question and associate it with this response.
        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith("question_"):
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in the
                # field name in the __init__ method of this form class.
                q_id = int(field_name.split("_")[1])
                q = Question.objects.get(pk=q_id)
                
                if q.question_type == Question.TEXT:
                    a = AnswerText(question = q)
                    a.body = field_value
                elif q.question_type == Question.RADIO:
                    a = AnswerRadio(question = q)
                    a.body = field_value
                        
                print "creating answer to question %d of type %s" % (q_id, a.question.question_type)
                print a.question.text
                print 'answer value:'
                print field_value
                a.response = response
                a.save()
        return response

