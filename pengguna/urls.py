from django.urls import path
from pengguna.views import (
    pengguna_list, 
    pengguna_edit,
    pengguna_delete, 
    )

urlpatterns = [
    path('pengguna/list/', pengguna_list, name='pengguna_list'),
    path('pengguna/edit/<int:id_user>',  pengguna_edit, name='pengguna_edit'),
    path('pengguna/delete/<int:id_user>', pengguna_delete, name='pengguna_delete'),
]
