from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from survey.models import Survey, UserSurvey, UserAnswerText, UserChoiceAnswer, QuestionTextAnswer, \
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

        return questions

    class Meta:
        model = Survey
        fields = (
            'id',
            'title',
            'date',
            'questions_text_answer',
            'questions_choice_answer',
        )


class QuestionTextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTextAnswer
        fields = '__all__'


class UserTextAnswerWriteSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=QuestionTextAnswer.objects.all()
    )

    class Meta:
        model = UserAnswerText
        fields = (
            'question',
            'answer',
        )


class UserTextAnswerReadSerializer(serializers.ModelSerializer):
    question = QuestionTextAnswerSerializer()

    class Meta:
        model = UserAnswerText
        fields = (
            'question',
            'answer',
        )


class AnswerChoiceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = (
            'id',
            'answer_text'
        )


class QuestionChoiceAnswerReadSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceReadSerializer(many=True)

    class Meta:
        model = QuestionChoiceAnswer
        fields = (
            'id',
            'question_text',
            'choices',
        )


class UserChoiceAnswerWriteSerializer(serializers.ModelSerializer):
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


class UserChoiceAnswerReadSerializer(serializers.ModelSerializer):
    question = QuestionChoiceAnswerReadSerializer()
    answer = AnswerChoiceReadSerializer(many=True)

    class Meta:
        model = UserChoiceAnswer
        fields = (
            'question',
            'answer',
        )


class UserSurveySerializer(serializers.ModelSerializer):
    survey = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    text_answers = UserTextAnswerWriteSerializer(many=True)
    choice_answers = UserChoiceAnswerWriteSerializer(many=True)

    class Meta:
        model = UserSurvey
        fields = (
            'survey',
            'user',
            'choice_answers',
            'text_answers',
        )

    def update(self, instance, validated_data):
        def validate_choice_answers(choice_answers_, text_answers_, instance_):
            all_answers_count = len(choice_answers_) + len(text_answers_)
            total_question_count = len(instance_.text_answers.all()) + len(instance_.choice_answers.all())

            if all_answers_count < total_question_count:
                ValidationError("You didn't answer all the questions", 400)
            elif all_answers_count > total_question_count:
                ValidationError("Wrong data: too many answers", 400)

        def validate_answers_or_raise_400(answers_, question_):
            if len(answers_) > question_.choices_count:
                raise ValidationError(
                    f'Too many choices for question {question_}. Max count {question_.choices_count}',
                    400
                )

            for answer in answers_:
                if answer not in question_.choices.all():
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


class UserSurveysListSerializer(serializers.ModelSerializer):
    survey = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='survey:surveys-detail'
        # queryset=UserSurvey.objects.all()
    )

    class Meta:
        model = UserSurvey
        fields = (
            'survey',
        )


class UserDetailSerializer(serializers.ModelSerializer):
    surveys = UserSurveysListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'surveys'
        )


class UserSurveyDetailSerializer(serializers.ModelSerializer):
    survey = SurveyListSerializer(read_only=True)
    text_answers = UserTextAnswerReadSerializer(many=True)
    choice_answers = UserChoiceAnswerReadSerializer(many=True)

    class Meta:
        model = UserSurvey
        fields = (
            'survey',
            'text_answers',
            'choice_answers'
        )
