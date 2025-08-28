import pytest
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire.settings')
django.setup()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_api_client(user):
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def user(user_factory):
    return user_factory()

@pytest.fixture
def user_factory():
    from tests.factories import CustomUserFactory
    return CustomUserFactory

@pytest.fixture
def question_factory():
    from tests.factories import QuestionFactory
    return QuestionFactory

@pytest.fixture
def answer_factory():
    from tests.factories import AnswerFactory
    return AnswerFactory