from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('equipos/', views.equipos, name='equipos'),
    path('partidos/', views.partidos, name='partidos'),
    path('tabla/', views.tabla, name='tabla'),
    path('finalista/', views.finalista, name='finalista'),
]
