import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Question, Answer
from .serializers import (
    QuestionSerializer,
    QuestionDetailSerializer,
    AnswerSerializer
)

logger = logging.getLogger('my_logger')


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        logger.info(f"Запрос на создание вопроса от пользователя: {request.user}")
        logger.debug(f"Данные для создания вопроса: {request.data}")
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Вопрос успешно создан с ID: {response.data.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Ошибка при создании вопроса: {str(e)}")
            raise


class QuestionDetailView(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def destroy(self, request, *args, **kwargs):
        question_id = kwargs.get('pk')
        logger.warning(f"Запрос на удаление вопроса ID: {question_id} от пользователя: {request.user}")
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Вопрос ID: {question_id} успешно удален")
            return response
        except Exception as e:
            logger.error(f"Ошибка при удалении вопроса ID: {question_id}: {str(e)}")
            raise


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        question_id = self.kwargs.get("id")
        logger.info(f"Запрос на создание ответа для вопроса ID: {question_id} от пользователя: {self.request.user}")
        
        try:
            question = Question.objects.get(pk=question_id)
            logger.debug(f"Вопрос ID: {question_id} найден")
        except Question.DoesNotExist:
            logger.error(f"Вопрос ID: {question_id} не найден при создании ответа")
            raise NotFound("Вопрос не найден")

        try:
            serializer.save(user=self.request.user, question=question)
            logger.info(f"Ответ успешно создан для вопроса ID: {question_id}")
        except Exception as e:
            logger.error(f"Ошибка при создании ответа для вопроса ID: {question_id}: {str(e)}")
            raise


class AnswerDetailView(generics.RetrieveDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        answer_id = kwargs.get('pk')
        logger.warning(f"Запрос на удаление ответа ID: {answer_id} от пользователя: {request.user}")
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Ответ ID: {answer_id} успешно удален")
            return response
        except Exception as e:
            logger.error(f"Ошибка при удалении ответа ID: {answer_id}: {str(e)}")
            raise