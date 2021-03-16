from typing import List

from django.db import models


class Survey(models.Model):
    """Опросник"""
    title = models.CharField(max_length=100)
    date = models.DateTimeField()

    def add_simple_question(self, question_text: str):
        return QuestionTextAnswer.objects.create(
            survey=self,
            question_text=question_text
        )
    add_simple_question.short_description = 'Add Simple Text Question'

    def add_question_choice(
            self,
            question_text: str,
            choices: List[str],
            choices_count: int = 1
    ) -> 'QuestionChoiceAnswer':
        if len(choices) > choices_count:
            raise ValueError

        question = QuestionChoiceAnswer.objects.create(
            question_text=question_text,
            survey=self,
            choices_count=choices_count,
        )
        for choice in choices:
            AnswerChoice.objects.create(
                question=question,
                answer_text=choice
            )

        return question
    add_question_choice.boolean = True

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
