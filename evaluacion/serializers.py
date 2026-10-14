from rest_framework import serializers
from .models import Proyecto, Evaluador, Calificacion, Evaluacion

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'equipo', 'categoria', 'evaluadores']

class EvaluadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluador
        fields = ['nombre', 'correo']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['evaluador', 'proyecto', 'puntaje']

class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = ['proyecto', 'evaluadores', 'calificaciones']