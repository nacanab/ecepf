from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Examen, QuestionExamen, ReponseExamen, ResultatExamen
from .serializers import ExamenSerializer, ResultatExamenSerializer

class ExamenListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExamenSerializer
    
    

    def get_queryset(self):
        return Examen.objects.filter(is_published=True)

class ExamenDetailView(generics.RetrieveAPIView):
    serializer_class = ExamenSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_object(self):
        return get_object_or_404(Examen, slug=self.kwargs['slug'])

class TakeExamenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, slug):
        examen = get_object_or_404(Examen, slug=slug)
        student = request.user.student
        answers = request.data.get('answers', [])
        
        score = 0
        total_questions = examen.questions.count()

        for answer in answers:
            question = get_object_or_404(QuestionExamen, id=answer['question_id'])
            
            if question.question_type == "multiple_choice":
                reponse = ReponseExamen.objects.filter(id=answer['answer'], question=question).first()
                if reponse and reponse.is_correct:
                    score += question.score
            elif question.question_type == "true_false":
                correct_answer = ReponseExamen.objects.filter(question=question, is_correct=True).first()
                if str(answer['answer']).lower() == str(correct_answer.content).lower():
                    score += question.score
            elif question.question_type == "short_answer":
                correct_answer = ReponseExamen.objects.filter(question=question, is_correct=True).first()
                if answer['answer'].strip().lower() == correct_answer.content.strip().lower():
                    score += question.score

        resultat = ResultatExamen.objects.create(
            student=student,
            examen=examen,
            score=score,
            is_passed=score >= examen.pass_mark,
            completed_at=timezone.now()
        )

        return Response({
            'score': score,
            'is_passed': resultat.is_passed,
            'max_score': examen.max_score
        }, status=status.HTTP_201_CREATED)

class ResultatListView(generics.ListAPIView):
    serializer_class = ResultatExamenSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ResultatExamen.objects.filter(student=self.request.user.student)

class ResultatDetailView(generics.RetrieveAPIView):
    serializer_class = ResultatExamenSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            ResultatExamen,
            examen__slug=self.kwargs['slug'],
            student=self.request.user.student
        )