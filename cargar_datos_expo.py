
import json
from pathlib import Path
from django.db import transaction
from evaluacion.models import Proyecto, Evaluador, Calificacion

ruta = Path("datos_expo.json")

with ruta.open("r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

with transaction.atomic():

    # 1. Crear evaluadores
    for dato in datos["evaluadores"]:
        Evaluador.objects.get_or_create(
            correo=dato["correo"],
            defaults={"nombre": dato["nombre"]}
        )

    # 2. Crear proyectos
    for dato in datos["proyectos"]:
        Proyecto.objects.get_or_create(
            titulo=dato["titulo"],
            defaults={
                "equipo": dato["equipo"],
                "categoria": dato["categoria"]
            }
        )

    # 3. Crear calificaciones y sus relaciones
    calificaciones_nuevas = 0

    for dato in datos["calificaciones"]:
        proyecto = Proyecto.objects.get(
            titulo=dato["proyecto_titulo"]
        )
        evaluador = Evaluador.objects.get(
            correo=dato["evaluador_correo"]
        )

        _, creada = Calificacion.objects.get_or_create(
            proyecto=proyecto,
            evaluador=evaluador,
            defaults={
                "puntaje": dato["puntaje"],
                "comentario": dato["comentario"]
            }
        )

        if creada:
            calificaciones_nuevas += 1

print("carga terminada :)")
print("Evaluadores:", Evaluador.objects.count())
print("Proyectos:", Proyecto.objects.count())
print("Calificaciones nuevas:", calificaciones_nuevas)
print("Total de calificaciones:", Calificacion.objects.count())
