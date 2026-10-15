
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from evaluacion.api_views import (
    ProyectoViewSet,
    EvaluadorViewSet,
    CalificacionViewSet,
)

router = DefaultRouter()
router.register("proyectos", ProyectoViewSet)
router.register("evaluadores", EvaluadorViewSet)
router.register("calificaciones", CalificacionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
