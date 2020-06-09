from django.urls import path
from .import views

urlpatterns = [
    path('',views.main_screen,name='main_screen'),
    path('<slug:id>/delete-my-list',views.delete,name='delete')
]