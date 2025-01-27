from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('createcourse/', views.UserLoginView.as_view(), name='course'),
    path('getcourses/', views.ListCourses.as_view({'get': 'list'}), name='courselist'),
    path('createcourse/', views.CreateCourseView.as_view(), name='courselist')

]
