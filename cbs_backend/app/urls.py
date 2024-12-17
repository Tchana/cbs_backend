from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_user_view, name= 'home'),
    path('showT/', views.showTeacherView, name='teacher-list'),
    path('showS/', views.showTeacherView, name='student-list'),
]
