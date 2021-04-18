from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('how_use', views.how_use),
    path('upload', views.upload),
    path('login', views.logining),
    path('register', views.register),
    path('logout', views.logout_view),
    path('prog/<str:prg_name>', views.prog),
    path('process_syntax/<str:prg_name>', views.process_syntax),
    path('delite/<str:p_name>', views.delite),
    path('syntax/<synt_id>', views.syntax),
    path('report/<p_id>', views.take_report),
    path('static/logo', views.get_logo)
]
