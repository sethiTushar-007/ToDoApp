from django.urls import path
from .import views

urlpatterns = [
    path('<slug:id>',views.checklist,name='checklist')
]