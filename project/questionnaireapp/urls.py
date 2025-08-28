from django.urls import path
from .views import (
    QuestionListCreateView,
    QuestionDetailView,
    AnswerCreateView,
    AnswerDetailView,
)

urlpatterns = [
    path("questions/<int:id>/answers/", AnswerCreateView.as_view(), name="answer-create"),
    path("answers/<int:pk>/", AnswerDetailView.as_view(), name="answer-detail"),

    path("questions/", QuestionListCreateView.as_view(), name="question-list"),
    path("questions/<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),

]
