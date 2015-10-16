from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
TEST_TYPE_CHOICES = (
                     ('PRETEST',
                      'PreTest'),
                     ('PSYCHO','Psycho'),
                     )

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=100)
    age = models.IntegerField()
    score_test = models.IntegerField(null=True)
    score_pre = models.IntegerField(null=True)
    score_post = models.IntegerField(null=True)
    
    def __str__(self):
        return self.email

class Test(models.Model):
    
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)

    def __unicode__(self):
        return (self.name)

    def questions(self):
        if self.pk:
            return Question.objects.filter(test=self.pk)
        else:
            return None

def validate_list(value):
	'''takes a text value and verifies that there is at least one comma '''
	values = value.split(',')
	if len(values) < 2:
		raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")

class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'

    QUESTION_TYPES = (
                  (TEXT, 'text'),
                  (RADIO, 'radio'),
                  )
    text = models.TextField()
    test = models.ForeignKey(Test)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    # the choices field is only used if the question type
    choices = models.TextField(blank=True, null=True,
        help_text='if the question type is "radio," provide a comma-separated list of options for this question .')
                                                 
    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO):
            validate_list(self.choices)
            super(Question, self).save(*args, **kwargs)
                                                 
    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
            for the 'choices' argument of a form widget.'''
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c,c))
            choices_tuple = tuple(choices_list)
        return choices_tuple
                                                 
    def __unicode__(self):
        return (self.text)

class Response(models.Model):
	# a response object is just a collection of questions and answers with a
	# unique interview uuid
	created = models.DateTimeField(auto_now_add=True)
	test = models.ForeignKey(Test)
	interview_uuid = models.CharField("Interview unique identifier", max_length=36)
    
	def __unicode__(self):
		return ("response %s" % self.interview_uuid)

class AnswerBase(models.Model):
	question = models.ForeignKey(Question)
	response = models.ForeignKey(Response)
	created = models.DateTimeField(auto_now_add=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
	body = models.TextField(blank=True, null=True)


