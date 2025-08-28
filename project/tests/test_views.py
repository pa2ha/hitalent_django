import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestQuestionViews:

    def test_question_list_get(self, api_client, question_factory):
        """Test GET /api/questions/"""
        question_factory.create_batch(3)

        url = reverse('question-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3
        assert len(response.data['results']) == 3

    def test_question_list_post_authenticated(self, authenticated_api_client, user):
        """Test POST /api/questions/ authenticated"""
        url = reverse('question-list')
        data = {
            'text': 'Test question text for creating a new question'
        }

        response = authenticated_api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']
        assert 'id' in response.data
        assert 'created_at' in response.data

    def test_question_list_post_unauthenticated(self, api_client):
        """Test POST /api/questions/ unauthenticated"""
        url = reverse('question-list')
        data = {'text': 'Test question'}

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_question_detail_get(self, api_client, question_factory):
        """Test GET /api/questions/{id}/"""
        question = question_factory()

        url = reverse('question-detail', kwargs={'pk': question.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == question.pk
        assert response.data['text'] == question.text

    def test_question_detail_delete_authenticated(self, authenticated_api_client, question_factory):
        """Test DELETE /api/questions/{id}/ by authenticated user"""
        question = question_factory()

        url = reverse('question-detail', kwargs={'pk': question.pk})
        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_question_detail_delete_unauthenticated(self, api_client, question_factory):
        """Test DELETE /api/questions/{id}/ unauthenticated"""
        question = question_factory()

        url = reverse('question-detail', kwargs={'pk': question.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_question_detail_nonexistent(self, api_client):
        """Test GET non-existent question"""
        url = reverse('question-detail', kwargs={'pk': 9999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAnswerViews:

    def test_answer_create_post_authenticated(self, authenticated_api_client, question_factory, user):
        """Test POST /api/questions/{id}/answers/"""
        question = question_factory()

        url = reverse('answer-create', kwargs={'id': question.pk})
        data = {
            'text': 'Test answer content for the question'
        }

        response = authenticated_api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']

    def test_answer_create_post_unauthenticated(self, api_client, question_factory):
        """Test POST /api/questions/{id}/answers/ unauthenticated"""
        question = question_factory()

        url = reverse('answer-create', kwargs={'id': question.pk})
        data = {'text': 'Test answer'}

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_answer_create_nonexistent_question(self, authenticated_api_client):
        """Test POST answer to non-existent question"""
        url = reverse('answer-create', kwargs={'id': 9999})
        data = {'text': 'Test answer'}

        response = authenticated_api_client.post(url, data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_answer_detail_get(self, api_client, answer_factory):
        """Test GET /api/answers/{id}/"""
        answer = answer_factory()

        url = reverse('answer-detail', kwargs={'pk': answer.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == answer.pk
        assert response.data['text'] == answer.text

    def test_answer_detail_delete_authenticated_owner(self, authenticated_api_client, answer_factory, user):
        """Test DELETE /api/answers/{id}/ by owner"""
        answer = answer_factory(user=user)

        url = reverse('answer-detail', kwargs={'pk': answer.pk})
        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_answer_detail_delete_unauthenticated(self, api_client, answer_factory):
        """Test DELETE /api/answers/{id}/ unauthenticated"""
        answer = answer_factory()

        url = reverse('answer-detail', kwargs={'pk': answer.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_answer_detail_nonexistent(self, api_client):
        """Test GET non-existent answer"""
        url = reverse('answer-detail', kwargs={'pk': 9999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
