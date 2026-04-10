import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from aplicacion.models import Equipo, Jugador

def update_data():
    teams_data = {
        "PSG": {
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/1200px-Paris_Saint-Germain_F.C..svg.png",
            "bg": "https://phantom-marca.unidadeditorial.es/70a3c200787e748cb9b6de1a70518349/assets/multimedia/imagenes/2022/07/04/16569476721590.jpg",
            "players": ["Mbappé", "Neymar", "Messi", "Marquinhos", "Donnarumma"]
        },
        "BAYER": {
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/5/59/Bayer_04_Leverkusen_logo.svg/1200px-Bayer_04_Leverkusen_logo.svg.png",
            "bg": "https://cdn.bayer04.de/20220721/mannschaftsfoto_22-23_3.jpg",
            "players": ["Musiala", "Sané", "Kimmich", "Gnabry", "Neuer"]
        },
        "ATHLETIC": {
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/9/98/Club_Athletic_Bilbao_logo.svg/1200px-Club_Athletic_Bilbao_logo.svg.png",
            "bg": "https://static.athletic-club.eus/wp-content/uploads/2023/10/WEB-EQUIPO-23-24.jpg",
            "players": ["Williams", "Muniain", "Sancet", "Yeray", "Simon"]
        },
        "CHELSEA": {
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/1200px-Chelsea_FC.svg.png",
            "bg": "https://www.chelseafc.com/content/dam/chelsea/main-team/men/2023-24/squad-photos/2023-24-SQUAD-PHOTO-LANDSCAPE.jpg",
            "players": ["Palmer", "Enzo", "Jackson", "Sterling", "Sanchez"]
        }
    }

    for name, data in teams_data.items():
        equipo, created = Equipo.objects.get_or_create(nombre=name)
        equipo.logo_url = data["logo"]
        equipo.background_url = data["bg"]
        equipo.save()

        # Delete existing players to match the image exactly
        equipo.jugadores.all().delete()
        
        for p_name in data["players"]:
            Jugador.objects.create(
                nombre=p_name,
                equipo=equipo,
                foto_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={p_name}"
            )
    
    print("Datos actualizados correctamente.")

if __name__ == "__main__":
    update_data()
