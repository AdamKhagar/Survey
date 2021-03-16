from rest_framework import serializers

from survey.models import Survey, QUESTION_TYPES


class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('get_questions', read_only=True)

    def get_questions(self, survey):
        questions = []
        for question in survey.question_text_answer.all():
            questions.append({
                'question_type': QUESTION_TYPES.TEXT_ANSWER,
                'question_id': question.pk,
                'question': question.question_text
            })
        for question in survey.question_choice_answer.all():
            questions.append({
                'question_type': QUESTION_TYPES.CHOICE_ANSWER,
                'question_id': question.pk,
                'question': question.question_text,
                'choices_count': question.choices_count,
                'choices': [{
                    'answer_id': answer.pk,
                    'answer': answer.answer_text
                    } for answer in question.choices.all()]
            })

        return questions

    class Meta:
        model = Survey
        fields = (
            'id',
            'title',
            'date',
            'questions'
        )
