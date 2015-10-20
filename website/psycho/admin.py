from django.contrib import admin

# Register your models here.
from psycho.models import User, Test, Question, AnswerText, AnswerRadio, Response, Activity

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'age')
    search_fields = ('email',)

admin.site.register(User, UserAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)

admin.site.register(Test, TestAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_type','text','test')
    list_filter = ('question_type',)
    search_fields = ('text',)

admin.site.register(Question, QuestionAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('test','user','created')
    list_filter = ('created','test')
    search_fields = ('user',)
admin.site.register(Response, ResponseAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response','question','body')
    search_fields = ('body',)

admin.site.register(AnswerText, AnswerAdmin)
admin.site.register(AnswerRadio, AnswerAdmin)

admin.site.register(Activity)