from django.contrib import admin

# Register your models here.
from psycho.models import User, Test, Question, AnswerText, AnswerRadio, Response

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'age', 'score_test', 'score_pre', 'score_post')
    list_filter = ('score_test',)
    search_fields = ('email',)

admin.site.register(User, UserAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)

admin.site.register(Test, TestAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('question_type',)
    search_fields = ('text',)

admin.site.register(Question, QuestionAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_filter = ('created','test','interview_uuid')
    search_fields = ('interview_uuid',)
admin.site.register(Response, ResponseAdmin)

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ('body',)

admin.site.register(AnswerText, AnswerAdmin)
admin.site.register(AnswerRadio, AnswerAdmin)

