from django.shortcuts import render, redirect
from .models import Equipo, Partido, TablaPosiciones, Usuario
from django.db.models import Q

def login_view(request):
    # Si ya está logueado, redirigir a equipos
    if "usuario_id" in request.session:
        return redirect("equipos")

    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        try:
            # Buscar el usuario en la tabla Usuario personalizada
            user = Usuario.objects.get(username=u, password=p)
            request.session["usuario_id"] = user.id
            request.session["username"] = user.username
            return redirect("equipos")
        except Usuario.DoesNotExist:
            return render(request, "aplicacion/login.html", {"error": "Usuario o contraseña incorrectos"})
    
    return render(request, "aplicacion/login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")

def equipos(request):
    if "usuario_id" not in request.session:
        return redirect("login")
    
    lista_equipos = Equipo.objects.all()
    return render(request, "aplicacion/equipos.html", {"equipos": lista_equipos})

def partidos(request):
    if "usuario_id" not in request.session:
        return redirect("login")
    
    if request.method == "POST":
        partido_id = request.POST.get("partido_id")
        goles_local = request.POST.get("goles_local")
        goles_visitante = request.POST.get("goles_visitante")
        
        if partido_id:
            try:
                partido = Partido.objects.get(id=partido_id)
                partido.goles_local = int(goles_local)
                partido.goles_visitante = int(goles_visitante)
                partido.finalizado = True
                partido.save()
                
                # Recalcular estadísticas
                actualizar_estadisticas()
            except Partido.DoesNotExist:
                pass

    lista_partidos = Partido.objects.all()
    return render(request, "aplicacion/partidos.html", {"partidos": lista_partidos})

def actualizar_estadisticas():
    # Limpiar y reconstruir para simplicidad
    TablaPosiciones.objects.all().delete()
    equipos_db = Equipo.objects.all()
    
    for equipo in equipos_db:
        tp = TablaPosiciones.objects.create(equipo=equipo)
        
        # Partidos como local
        locales = Partido.objects.filter(equipo_local=equipo, finalizado=True)
        for p in locales:
            tp.jugados += 1
            if p.goles_local > p.goles_visitante:
                tp.ganados += 1
                tp.puntos += 3
            elif p.goles_local == p.goles_visitante:
                tp.empatados += 1
                tp.puntos += 1
            else:
                tp.perdidos += 1
        
        # Partidos como visitante
        visitantes = Partido.objects.filter(equipo_visitante=equipo, finalizado=True)
        for p in visitantes:
            tp.jugados += 1
            if p.goles_visitante > p.goles_local:
                tp.ganados += 1
                tp.puntos += 3
            elif p.goles_visitante == p.goles_local:
                tp.empatados += 1
                tp.puntos += 1
            else:
                tp.perdidos += 1
        
        tp.save()

def tabla(request):
    if "usuario_id" not in request.session:
        return redirect("login")
    
    estadisticas = TablaPosiciones.objects.all().order_by("-puntos")
    return render(request, "aplicacion/tabla.html", {"estadisticas": estadisticas})

def finalista(request):
    if "usuario_id" not in request.session:
        return redirect("login")
    
    # El que tiene más puntos es el finalista
    ganador = TablaPosiciones.objects.all().order_by("-puntos").first()
    equipo_ganador = ganador.equipo if ganador else None
    
    return render(request, "aplicacion/finalista.html", {"finalista": equipo_ganador})