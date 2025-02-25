"""
URL configuration for cbs_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from backend.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('request_reset', RequestPasswordReset.as_view(), name='r_resetpwd'),
    path('reset/<token>', ResetPassword.as_view(), name='r_resetpwd'),
    
    path('course/create', CreateCourseView.as_view(), name='c_course'),
    path('course/get', GetListCourses.as_view(), name='g_course'),
    path('course/edit/<uuid>', UpdateCourseView.as_view(), name='u_course'),
    path('course/enroll', EnrollView.as_view(), name='subcourse'),
    
    path('lesson/add', AddLessonView.as_view(), name='c_lesson'),
    path('lesson/get/<uuid>', GetLesson.as_view(), name='g_lesson'),
    
    path('user/', GetAllUserView.as_view(), name='g_user'),
    path('user/me', GetMe.as_view(), name='g_p'),
    path('user/<uuid>', DeleteUser.as_view(), name='d_user'),
    
    path('user/edit/<uuid>', EditUserProfileView().as_view(), name='e_user'),
    path('user/teachers', GetTeacherView.as_view(), name='g_teacher'),
    path('user/students', GetStudentView.as_view(), name='g_student'),
    
    path('book', AddBookView.as_view(), name="a_book"),
    path('book', GetBookView.as_view({'get': 'list'}), name="g_book"),
    
    path('audio', AddAudioView.as_view(), name='a_audio'),
    path('video', AddVideoView.as_view(), name='a_video') 
]
