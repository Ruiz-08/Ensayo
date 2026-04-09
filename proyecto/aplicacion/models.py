from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    nombre = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')

    def __str__(self):
        return f"{self.nombre} ({self.equipo.nombre})"


class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, models.CASCADE, related_name='partidos_visitante')
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"


class TablaPosiciones(models.Model):
    equipo = models.ForeignKey(Equipo, models.CASCADE)
    jugados = models.IntegerField(default=0)
    ganados = models.IntegerField(default=0)
    empatados = models.IntegerField(default=0)
    perdidos = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return f"Tabla: {self.equipo.nombre}"


class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
