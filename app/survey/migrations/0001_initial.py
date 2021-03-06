# Generated by Django 3.1.7 on 2021-03-16 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionChoiceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('choices_count', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionTextAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='UserSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveyed_users', to='survey.survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='survey.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserChoiceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ManyToManyField(to='survey.AnswerChoice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_choice_answers', to='survey.questionchoiceanswer')),
                ('user_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice_answers', to='survey.usersurvey')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswerText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_text_answers', to='survey.questiontextanswer')),
                ('user_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_answers', to='survey.usersurvey')),
            ],
        ),
        migrations.AddField(
            model_name='questiontextanswer',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_text_answer', to='survey.survey'),
        ),
        migrations.AddField(
            model_name='questionchoiceanswer',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_choice_answer', to='survey.survey'),
        ),
        migrations.AddField(
            model_name='answerchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='survey.questionchoiceanswer'),
        ),
    ]
