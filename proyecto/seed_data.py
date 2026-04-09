import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from aplicacion.models import Equipo, Jugador, Partido, TablaPosiciones
from aplicacion.views import actualizar_estadisticas

def seed():
    # Clear existing data
    print("Limpiando datos existentes...")
    TablaPosiciones.objects.all().delete()
    Partido.objects.all().delete()
    Jugador.objects.all().delete()
    Equipo.objects.all().delete()

    # Create Teams
    teams_data = [
        {"nombre": "PSG", "jugadores": ["Mbappe", "Neymar", "Messi", "Marquinhos", "Donnarumma"]},
        {"nombre": "BAYER", "jugadores": ["Musiala", "Sane", "Kimmich", "Gnabry", "Neuer"]},
        {"nombre": "ATHLETIC", "jugadores": ["Williams", "Muniain", "Sancet", "Yeray", "Simon"]},
        {"nombre": "CHELSEA", "jugadores": ["Palmer", "Enzo", "Jackson", "Sterling", "Sanchez"]},
    ]

    teams = {}
    for t_data in teams_data:
        team = Equipo.objects.create(nombre=t_data["nombre"])
        teams[t_data["nombre"]] = team
        print(f"Equipo creado: {team.nombre}")
        for j_name in t_data["jugadores"]:
            Jugador.objects.create(nombre=j_name, equipo=team)
            print(f"  Jugador creado: {j_name}")

    # Create Matches
    matches_data = [
        ("PSG", "BAYER", 2, 1, True),
        ("ATHLETIC", "CHELSEA", 0, 0, True),
        ("PSG", "ATHLETIC", 3, 0, True),
        ("BAYER", "CHELSEA", 1, 2, True),
        ("PSG", "CHELSEA", 1, 1, True),
        ("BAYER", "ATHLETIC", 2, 0, True),
    ]

    for loc, vis, gl, gv, fin in matches_data:
        p = Partido.objects.create(
            equipo_local=teams[loc],
            equipo_visitante=teams[vis],
            goles_local=gl,
            goles_visitante=gv,
            finalizado=fin
        )
        print(f"Partido registrado: {p.equipo_local} {p.goles_local} - {p.goles_visitante} {p.equipo_visitante}")

    # Update Statistics
    print("Actualizando tabla de posiciones...")
    actualizar_estadisticas()
    print("¡Base de datos sembrada con éxito!")

if __name__ == "__main__":
    seed()
