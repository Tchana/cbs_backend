from django.urls import path
from . import views

urlpatterns = [
    path('getLesson/', views.getLesson),
    path('addLesson/', views.addLesson),
    path('getBooks/', views.getBooks), 
]
