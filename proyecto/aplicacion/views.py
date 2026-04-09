from django.shortcuts import render, redirect
from .models import Torneo, Equipo, Partido
from django.db.models import Q
# Create your views here.


def menu(request):
    if not request.session.get("usuario"):
        return redirect("login")

    torneos = Torneo.objects.all()

    return render(request, "menu.html", {"torneos": torneos})

def crear_torneo(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        torneo = Torneo.objects.create(nombre=nombre)

        return redirect("equipos", torneo_id=torneo.id)

    return render(request, "crear_torneo.html")

def agregar_equipos(request, torneo_id):
    torneo = Torneo.objects.get(id=torneo_id)

    if request.method == "POST":
        nombre=request.POST.get("nombre")
        Equipo.objects.create(nombre=nombre, torneo=torneo)

    equipos = Equipo.objects.filter(torneo=torneo)

    return render(request, "equipos.html", {"torneo": torneo, "equipos": equipos})

def generar_fixture(torneo):
    equipos = list(Equipo.objects.filter(torneo=torneo))

    for i in range(len(equipos)):
        for j in range(i+1,len(equipos)):
            Partido.objects.create(torneo=torneo,
            equipo_local=equipos[i],
            equipo_visitante=equipos[j])

def crear_fixture(request, torneo_id):
    torneo = Torneo.objects.get(id=torneo_id)

    generar_fixture(torneo)

    return redirect("ver_partidos", torneo_id=torneo.id)

def ver_partidos(request, torneo_id):
    partidos = Partido.objects.filter(torneo_id=torneo_id)

    return render(request, "partidos.html", {"partidos":partidos})

def registrar_resultado(request, partido_id):
    partido = Partido.objects.get(id=partido_id)

    if request.method == "POST":
        partido.goles_local = int(request.POST.get("goles_local"))
        partido.goles_visitante = int(request.POST.get("goles_visitante"))
        partido.jugado = True
        partido.save()

        return render(request, "registrar.html", {"partido":partido})
    

def tabla_posiciones(request, torneo_id):
    equipos = Equipo.objects.filter(torneo_id=torneo_id)

    tabla = []

    for equipo in equipos:
        partidos = Partido.objects.filter(Q(equipo_local=equipo) | Q(equipo_visitante=equipo), jugado=True)

    jugados = ganados = empatados = perdidos = puntos = 0

    for p in partidos:
        jugados += 1

        if p.equipo_local == equipo:
            gf=p.goles_local
            gc=p.goles_visitante
        else:
            gf=p.goles_visitante
            gc=p.goles_local

        if gf > gc:
            ganados += 1
            puntos += 3
        elif gf == gc:
            empatados += 1
            puntos += 1
        else:
            perdidos += 1

    tabla.append({
    "equipo":equipo.nombre,
    "jugados":jugados,
    "ganados":ganados,
    "empatados":empatados,
    "perdidos":perdidos,
    "puntos":puntos})

    tabla.sort(key=lambda x: -x["puntos"])

    return render(request, "tabla.html", {"tabla":tabla})