from typing import List

from django.db import models


class Survey(models.Model):
    """Опросник"""
    title = models.CharField(max_length=100)
    date = models.DateTimeField()


class QuestionBase(models.Model):
    """Базовый класс вопроса"""
    question_text = models.TextField()

    class Meta:
        abstract = True


class QuestionTextAnswer(QuestionBase):
    """Вопрос с текстовым отвертом"""
    survey = models.ForeignKey(
        Survey,
        related_name='question_text_answer',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'#{self.pk}:QuestionText {self.question_text}'


class QuestionChoiceAnswer(QuestionBase):
    """Вопрос с вариантами ответа"""
    choices_count = models.IntegerField()

    survey = models.ForeignKey(
        Survey,
        related_name='question_choice_answer',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'#{self.pk}:QuestionChoice {self.choices_count} {self.question_text}'


class AnswerChoice(models.Model):
    """Возможные варианты ответа"""
    question = models.ForeignKey(
        QuestionChoiceAnswer,
        related_name='choices',
        on_delete=models.CASCADE,
    )
    answer_text = models.TextField()


class QUESTION_TYPES:
    TEXT_ANSWER = 'text'
    CHOICE_ANSWER = 'choice'

    CHOICES = (
        (TEXT_ANSWER, QuestionTextAnswer),
        (CHOICE_ANSWER, QuestionChoiceAnswer)
    )


class User(models.Model):
    """Пользователь"""
    email = models.EmailField(blank=True)


class UserSurvey(models.Model):
    user = models.ForeignKey(
        User,
        related_name='surveys',
        on_delete=models.CASCADE
    )
    survey = models.ForeignKey(
        Survey,
        related_name='surveyed_users',
        on_delete=models.CASCADE
    )


class UserAnswerText(models.Model):
    """Текстовый ответ"""
    user_survey = models.ForeignKey(
        UserSurvey,
        related_name='text_answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        QuestionTextAnswer,
        related_name='users_text_answers',
        on_delete=models.CASCADE,
    )
    answer = models.TextField()


class UserChoiceAnswer(models.Model):
    """Ответ на вопрос вариантами ответа"""
    user_survey = models.ForeignKey(
        UserSurvey,
        related_name='choice_answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        QuestionChoiceAnswer,
        related_name='users_choice_answers',
        on_delete=models.CASCADE,
    )
    answer = models.ManyToManyField(AnswerChoice)
