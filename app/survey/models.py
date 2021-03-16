from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class QuestionBase(models.Model):
    """Базовый класс вопроса"""
    question_text = models.TextField()


class QuestionTextAnswer(QuestionBase):
    """Вопрос с текстовым отвертом"""
    answer = models.TextField()

    def __str__(self):
        return f'#{self.pk}:QuestionText {self.question_text}'


class QuestionChoiceAnswer(QuestionBase):
    """Вопрос с вариантами ответа"""
    choices_count = models.IntegerField()

    def __str__(self):
        return f'#{self.pk}:QuestionChoice {self.choices_count} {self.question_text}'


class AnswerChoice(models.Model):
    """Возможные варианты ответа"""
    question = models.ForeignKey(
        QuestionChoiceAnswer,
        related_name='choices',
        on_delete=models.CASCADE,
    )
    answer = models.TextField()


class Survey(models.Model):
    """Опросник"""
    title = models.CharField(max_length=100)
    date = models.DateTimeField()

    def add_question(self, question: QuestionBase) -> 'SurveyQuestion':
        question_type = ContentType.objects.get_for_model(question)

        return SurveyQuestion.objects.create(
            survey=self,
            question_type=question_type,
            question_object_id=question.pk
        )


class SurveyQuestion(models.Model):
    """Many to many"""
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    question_object_id = models.IntegerField()
    question_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    question = GenericForeignKey(
        'question_type',
        'question_object_id',
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


class UserAnswerBase(models.Model):
    """Базовый класс ответа"""
    user_survey = models.ForeignKey(
        UserSurvey,
        related_name='answers',
        on_delete=models.CASCADE
    )


class UserAnswerText(UserAnswerBase):
    """Текстовый ответ"""
    question = models.ForeignKey(
        QuestionTextAnswer,
        related_name='users_answers',
        on_delete=models.CASCADE,
    )
    answer = models.TextField()


class UserOneChoiceAnswer(UserAnswerBase):
    """Ответ на вопрос вариантами ответа"""
    question = models.ForeignKey(
        QuestionChoiceAnswer,
        related_name='users_answers',
        on_delete=models.CASCADE,
    )
    answer = models.ManyToManyField(AnswerChoice)
