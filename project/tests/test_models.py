import pytest

@pytest.mark.django_db
def test_question_creation(question_factory):
    """Test Question model creation"""
    from questionnaireapp.models import Question
    question = question_factory()
    assert isinstance(question, Question)
    assert question.text is not None
    assert question.created_at is not None
    assert str(question).startswith('Question')

@pytest.mark.django_db
def test_answer_creation(answer_factory):
    """Test Answer model creation"""
    from questionnaireapp.models import Answer
    answer = answer_factory()
    assert isinstance(answer, Answer)
    assert answer.text is not None
    assert answer.created_at is not None
    assert answer.question is not None
    assert answer.user is not None
    assert str(answer).startswith('Answer')

@pytest.mark.django_db
def test_question_answers_relationship(question_factory, answer_factory):
    """Test Question-Answer relationship"""
    from questionnaireapp.models import Question
    question = question_factory()
    answer1 = answer_factory(question=question)
    answer2 = answer_factory(question=question)
    
    assert question.answers.count() == 2
    assert answer1 in question.answers.all()
    assert answer2 in question.answers.all()

@pytest.mark.django_db
def test_user_answers_relationship(user_factory, answer_factory):
    """Test User-Answer relationship"""
    from Users.models import CustomUser
    user = user_factory()
    answer1 = answer_factory(user=user)
    answer2 = answer_factory(user=user)
    
    assert user.answers.count() == 2
    assert answer1 in user.answers.all()
    assert answer2 in user.answers.all()