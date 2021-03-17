from abc import ABC

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from survey.models import Survey, QUESTION_TYPES, UserSurvey, UserAnswerText, UserChoiceAnswer, QuestionTextAnswer, \
    QuestionChoiceAnswer, AnswerChoice

from survey.models import User


class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions_text_answer = serializers.SerializerMethodField(
        'get_questions_text_answer',
        read_only=True
    )
    questions_choice_answer = serializers.SerializerMethodField(
        'get_questions_choice_answer',
        read_only=True
    )

    def get_questions_choice_answer(self, survey):
        questions = []
        for question in survey.question_choice_answer.all():
            questions.append({
                'question_id': question.pk,
                'question': question.question_text,
                'choices_count': question.choices_count,
                'choices': [{
                    'answer_id': answer.pk,
                    'answer': answer.answer_text
                    } for answer in question.choices.all()]
            })

        return questions

    def get_questions_text_answer(self, survey):
        questions = []
        for question in survey.question_text_answer.all():
            questions.append({
                'question_id': question.pk,
                'question': question.question_text
            })

    class Meta:
        model = Survey
        fields = (
            'id',
            'title',
            'date',
            'questions_text_answer',
            'questions_choice_answer',
        )


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AnswerSerializerBase(serializers.RelatedField, ABC):
    def __init__(self, user_survey: UserSurvey, **kwargs):
        self.user_survey = user_survey
        super().__init__(**kwargs)


# class TextAnswerSerializer(AnswerSerializerBase):
#     queryset = UserAnswerText.objects.all()
#
#     def to_representation(self, value):
#         return {
#             "question_id": value.question.pk,
#             "question": value.question.question_text,
#             "answer_id": value.pk,
#             "answer": value.answer,
#         }
#
#     def to_internal_value(self, data):
#         try:
#             answer = UserAnswerText.objects.create(
#                 user_survey=self.user_survey,
#                 question=QuestionTextAnswer.objects.get(
#                     pk=int(data['question_id'])
#                 ),
#                 answer=data['answer'],
#             )
#         except QuestionTextAnswer.DoesNotExist:
#             raise ValidationError
#         else:
#             return answer
#
#
# class ChoiceAnswerSerializer(AnswerSerializerBase):
#     queryset = UserChoiceAnswer.objects.all()
#
#     def to_representation(self, value):
#         return {
#             "question_id": value.question.pk,
#             "question": value.question.question_text,
#             "answer_id": value.pk,
#             "answer": value.answer
#         }
#s
#     def to_internal_value(self, data):
#         try:
#             answer = UserChoiceAnswer.objects.create(
#                 user_survey=self.user_survey,
#                 question=QuestionChoiceAnswer.objects.get(
#                     pk=int(data['question_id'])
#                 ),
#                 answer=AnswerChoice.objects.filter(
#                     pk__in=data['answer']
#                 )
#             )
#         except ObjectDoesNotExist:
#             raise ValidationError()
#         else:
#             return answer

class UserTextAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=QuestionTextAnswer.objects.all()
    )

    class Meta:
        model = UserAnswerText
        fields = (
            'question',
            'answer',
        )


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = '__all__'


class UserChoiceAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=QuestionChoiceAnswer.objects.all()
    )
    answer = serializers.PrimaryKeyRelatedField(
        queryset=AnswerChoice.objects.all(),
        many=True
    )

    def validate_answer(self, answer):
        if len(answer) == 0:
            raise ValidationError('No have answers', 400)

        return answer

    class Meta:
        model = UserChoiceAnswer
        fields = (
            'question',
            'answer',
        )


class UserSurveySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    text_answers = UserTextAnswerSerializer(many=True)
    choice_answers = UserChoiceAnswerSerializer(many=True)

    class Meta:
        model = UserSurvey
        fields = (
            'user',
            'choice_answers',
            'text_answers',
        )

    def update(self, instance, validated_data):
        def validate_choice_answers(choice_answers, text_answers, instance):
            all_answers_count = len(choice_answers) + len(text_answers)
            total_question_count = len(instance.text_answers.all()) + len(instance.choice_answers.all())

            if all_answers_count < total_question_count:
                error = "You didn't answer all the questions"
            elif all_answers_count > total_question_count:
                error = "Wrong data: too many answers"

            if error:
                raise ValidationError(error, 400)

        def validate_answers_or_raise_400(answers, question):
            if len(answers) > question.choices_count:
                raise ValidationError(
                    f'Too many choices for question {question}. Max count {question.choices_count}',
                    400
                )

            for answer in answers:
                if answer not in question.choices.all():
                    raise ValidationError(
                        'The question does not have this option in the list of possible answers',
                        400
                    )

        choice_answers_ordered_dict = validated_data.pop('choice_answers')
        choice_answers = []
        for item in choice_answers_ordered_dict:
            question = item['question']

            user_choice_answer = UserChoiceAnswer.objects.create(
                user_survey=instance,
                question=question
            )

            answers = item['answer']
            validate_answers_or_raise_400(answers, question)
            user_choice_answer.answer.set(item['answer'])

            user_choice_answer.save()
            choice_answers.append(user_choice_answer)

        instance.choice_answers.set(choice_answers)

        text_answers_ordered_dict = validated_data.pop('text_answers')
        text_answers = [UserAnswerText.objects.create(
            user_survey=instance,
            question=item['question'],
            answer=item['answer']
            ) for item in text_answers_ordered_dict]

        instance.text_answers.set(text_answers)

        validate_choice_answers(choice_answers, text_answers, instance)
        instance.save()
        return instance


