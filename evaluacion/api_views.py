from django.db.models import Count
from rest_framework import viewsets

from .models import Proyecto, Evaluador, Calificacion
from .serializers import ProyectoSerializer, EvaluadorSerializer, CalificacionSerializer