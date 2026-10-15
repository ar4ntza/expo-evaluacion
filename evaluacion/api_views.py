from django.db.models import Count, Avg
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Proyecto, Evaluador, Calificacion
from .serializers import ProyectoSerializer, EvaluadorSerializer, CalificacionSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all().order_by("titulo")
    serializer_class = ProyectoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        titulo = self.request.query_params.get("titulo")
        equipo = self.request.query_params.get("equipo")
        categoria = self.request.query_params.get("categoria")
        evaluador = self.request.query_params.get("evaluador")

        # filtros de busqueda para proyectos
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if equipo:
            queryset = queryset.filter(equipo__icontains=equipo)

        return queryset.distinct()


class EvaluadorViewSet(viewsets.ModelViewSet):
    queryset = Evaluador.objects.all().order_by("nombre")
    serializer_class = EvaluadorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        nombre = self.request.query_params.get("nombre")
        correo = self.request.query_params.get("correo")

        # filtros de busqueda para evaluadores
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if correo:
            queryset = queryset.filter(correo__icontains=correo)

        return queryset


class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.select_related(
        "proyecto", "evaluador"
    ).all().order_by("-fecha")
    serializer_class = CalificacionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        proyecto = self.request.query_params.get("proyecto")
        evaluador = self.request.query_params.get("evaluador")
        puntaje_min = self.request.query_params.get("puntaje_min")
        puntaje_max = self.request.query_params.get("puntaje_max")

        # filtros de busqueda para calificaciones
        if proyecto:
            queryset = queryset.filter(proyecto_id=proyecto)
        if evaluador:
            queryset = queryset.filter(evaluador_id=evaluador)
        if puntaje_min:
            queryset = queryset.filter(puntaje__gte=puntaje_min)
        if puntaje_max:
            queryset = queryset.filter(puntaje__lte=puntaje_max)

        return queryset

class StatsViewSet(viewsets.ViewSet):

    def list(self, request):

        # 1. total de proyectos
        total_proyectos = Proyecto.objects.count()

        # 2. promedio de calificacion por categoria
        promedio_por_categoria = (
            Proyecto.objects.values("categoria")
            .annotate(
                total_proyectos=Count("id"),
                promedio=Avg("calificaciones__puntaje")
            )
            .order_by("categoria")
        )

        categorias = {
            codigo: etiqueta
            for codigo, etiqueta in Proyecto.Categoria.choices
        }

        stats_categoria = [
            {
                "categoria": categorias.get(
                    item["categoria"], item["categoria"]
                ),
                "codigo": item["categoria"],
                "total_proyectos": item["total_proyectos"],
                "promedio": (
                    round(float(item["promedio"]), 2)
                    if item["promedio"] is not None
                    else None
                ),
            }
            for item in promedio_por_categoria
        ]

        # 3. ordenar de puntaje maximo a minimo
        puntajes_desc = (
            Proyecto.objects.annotate(
                promedio=Avg("calificaciones__puntaje")
            )
            .filter(promedio__isnull=False)
            .order_by("-promedio", "titulo")
        )

        # 4. ordenar de puntaje minimo a maximo
        puntajes_asc = (
            Proyecto.objects.annotate(
                promedio=Avg("calificaciones__puntaje")
            )
            .filter(promedio__isnull=False)
            .order_by("promedio", "titulo")
        )

        def proyectos_ordenados(queryset):
            return [
                {
                    "id": proyecto.id,
                    "titulo": proyecto.titulo,
                    "equipo": proyecto.equipo,
                    "categoria": proyecto.get_categoria_display(),
                    "promedio": round(float(proyecto.promedio), 2),
                }
                for proyecto in queryset
            ]

        return Response({
            "total_proyectos": total_proyectos,
            "promedio_por_categoria": stats_categoria,
            "puntaje_maximo_a_minimo": proyectos_ordenados(
                puntajes_desc
            ),
            "puntaje_minimo_a_maximo": proyectos_ordenados(
                puntajes_asc
            ),
        })
