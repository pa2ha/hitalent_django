import factory
import uuid
from factory.django import DjangoModelFactory
from django.utils import timezone
from questionnaireapp.models import Question, Answer
from Users.models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_active = True
    position = factory.Faker('job')
    name = factory.Faker('name')


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question
        skip_postgeneration_save = True

    text = factory.Faker('text', max_nb_chars=500)
    created_at = factory.LazyFunction(timezone.now)


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer
        skip_postgeneration_save = True

    question = factory.SubFactory(QuestionFactory)
    user = factory.SubFactory(CustomUserFactory)
    text = factory.Faker('text', max_nb_chars=300)
    created_at = factory.LazyFunction(timezone.now)