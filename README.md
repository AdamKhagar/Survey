# Survey

# Quick start

1. Install ```pipenv``` (you can do that via ```pip```)
2. ```git clone https://github.com/AdamKhagar/Survey.git```
3. Install requierements:
    ``` 
    pipenv install -d --pre 
    pipenv shell 
    ```
4. Initiate the database: ```cd app && python manage.py migrate```
5. Create superuser: ```python manage.py createsuper``` 
6. Runserver: ```python manage.py runserver 8000```

# About API

You can find out about the api by using the **Swagger** ```localhost:8000:api/doc```

* To work with the api you need to get the user ID. This can be done by sending a POST request to ```api/user``` with:
  ```
  {
    "email": "user@gmail.com"
  }
  ```
* To save the results of the user survey you need to send a POST request to ```api/surveys/<int: survey_id>/save_user_answer``` with:
  ```
  {
    "user": <int: user_ID>,
    "choice_answers": [
      {
        "question": <int: question_ID>,
        "answer": [<int: answer_id>],
      }
    ],
    "text_answers": [
      {
        "question": <int: question_ID>,
        "answer": "string",
      }
    ]
  }   
  ```
* **Note!** Selector questions and textbox questions are two different entities, and so are their answers 

# Possible problems with swagger
On startup you may get an error : 
```diff
- Django TemplateSyntaxError - 'staticfiles' is not a registered tag library
```

Solutions [here](https://stackoverflow.com/questions/55929472/django-templatesyntaxerror-staticfiles-is-not-a-registered-tag-library)
