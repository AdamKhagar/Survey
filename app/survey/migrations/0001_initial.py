# Generated by Django 3.1.7 on 2021-03-16 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='UserAnswerBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey.usersurvey')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionTextAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_text_answer', to='survey.survey')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionChoiceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('choices_count', models.IntegerField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_choice_answer', to='survey.survey')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnswerChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='survey.questionchoiceanswer')),
            ],
        ),
        migrations.CreateModel(
            name='UserOneChoiceAnswer',
            fields=[
                ('useranswerbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.useranswerbase')),
                ('answer', models.ManyToManyField(to='survey.AnswerChoice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_answers', to='survey.questionchoiceanswer')),
            ],
            bases=('survey.useranswerbase',),
        ),
        migrations.CreateModel(
            name='UserAnswerText',
            fields=[
                ('useranswerbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.useranswerbase')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_answers', to='survey.questiontextanswer')),
            ],
            bases=('survey.useranswerbase',),
        ),
    ]