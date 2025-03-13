from rest_framework import serializers
from .models import Examen, QuestionExamen, ReponseExamen, ResultatExamen
from rest_framework.permissions import AllowAny

class ReponseExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReponseExamen
        fields = ['id', 'content']
        permission_classes = [AllowAny]

class QuestionExamenSerializer(serializers.ModelSerializer):
    reponses = ReponseExamenSerializer(many=True, read_only=True)
    permission_classes = [AllowAny]

    class Meta:
        model = QuestionExamen
        fields = ['id', 'content', 'question_type', 'score', 'reponses']

class ExamenSerializer(serializers.ModelSerializer):
    questions = QuestionExamenSerializer(many=True, read_only=True)
    permission_classes = [AllowAny]
    

    class Meta:
        model = Examen
        fields = '__all__'
        depth = 1

class ResultatExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultatExamen
        fields = '__all__'
        read_only_fields = ['student', 'examen', 'score', 'is_passed', 'started_at', 'completed_at']
        permission_classes = [AllowAny]