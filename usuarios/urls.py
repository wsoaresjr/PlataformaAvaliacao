# usuarios/urls.py
from django.urls import path
from . import views
from .views import resultados_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('gerenciar_usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('editar_usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('excluir_usuario/<int:pk>/', views.excluir_usuario, name='excluir_usuario'),
    path('dashboard_estudantes/', views.dashboard_estudantes, name='dashboard_estudantes'),
    path('instrucoes_avaliacao/<str:disciplina>/', views.instrucoes_avaliacao, name='instrucoes_avaliacao'),
    path('avaliacao/<str:disciplina>/', views.avaliacao, name='avaliacao'),
    path('finalizar_avaliacao/<str:disciplina>/', views.finalizar_avaliacao, name='finalizar_avaliacao'),
    path('resultados/', resultados_view, name='resultados'),


]

