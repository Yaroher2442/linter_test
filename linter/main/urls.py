from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('how_use', views.how_use),
    path('upload', views.upload),
    path('login',views.logining),
    path('register',views.register),
    path('logout',views.logout_view),
    path('prog/<str:prg_name>', views.prog),
    path('process_syntax/<str:prg_name>',views.process_syntax),
    # path('download', views.download_file),
    # path('download/<str:p_name>', views.file_send),
    path('delite/<str:p_name>',views.delite)
]