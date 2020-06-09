from django.urls import path
from .import views

urlpatterns = [
    path('<slug:id>',views.share,name='share'),   
]