from django.urls import path
from .views import *

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', home),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('user', GetAllUserView.as_view(), name='g_user'),
    
    path('user/edit/<uuid>', EditUserProfileView().as_view(), name='e_user'),
    path('user/teachers', GetTeacherView.as_view(), name='g_teacher'),
    path('user/students', GetStudentView.as_view(), name='g_student'),
     
    path('request_reset', RequestPasswordReset.as_view(), name='r_resetpwd'),
    path('reset/<token>', ResetPassword.as_view(), name='r_resetpwd'),
    
    path('course', CourseManagerView.as_view()),
    path('course/edit/<uuid>', UpdateCourseView.as_view(), name='u_course'),
    path('course/enroll', EnrollView.as_view(), name='subcourse'),
    
    path('lesson', LessonManagerView.as_view(), name='c_lesson'),
    path('lesson/get/<uuid>', GetLesson.as_view(), name='g_lesson'),
    
    path('user/me', GetMe.as_view(), name='g_p'),
    path('user/<uuid>', DeleteUser.as_view(), name='d_user'),
    
   
    path('book', AddBookView.as_view(), name="a_book"),
    path('book', GetBookView.as_view({'get': 'list'}), name="g_book"),
    
    path('audio', AddAudioView.as_view(), name='a_audio'),
    path('video', AddVideoView.as_view(), name='a_video') 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
