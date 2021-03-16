from django.contrib import admin
from django.forms import ModelForm

from . import models


class QuestionTextAnswerInline(admin.TabularInline):
    model = models.QuestionTextAnswer
    extra = 1


class QuestionChoiceAnswerInline(admin.TabularInline):
    model = models.QuestionChoiceAnswer
    extra = 1


class SurveyDataCreateOrReadOnly(ModelForm):
    class Meta:
        model = models.Survey
        exclude = ('date',)


class SurveyAdmin(admin.ModelAdmin):
    inlines = [
        QuestionTextAnswerInline,
        QuestionChoiceAnswerInline,
    ]

    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj:
            kwargs['form'] = SurveyDataCreateOrReadOnly
        return super().get_form(request, obj, **kwargs)


admin.site.register(models.Survey, SurveyAdmin)


class AnswerChoiceInline(admin.TabularInline):
    model = models.AnswerChoice
    extra = 4


class QuestionChoiceAnswer(admin.ModelAdmin):
    inlines = [
        AnswerChoiceInline
    ]


admin.site.register(models.QuestionChoiceAnswer, QuestionChoiceAnswer)

admin.site.register(models.QuestionTextAnswer)
