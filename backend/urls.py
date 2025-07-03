from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'course', CourseView, basename='course')
router.register(r'lesson', LessonView, basename='lesson')
router.register(r'book', BookView, basename='book_management')
router.register(r'user', UserView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('teachers/', GetTeacherView.as_view(), name='g_teacher'),
    path('students/', GetStudentView.as_view(), name='g_student'),
    path('me', GetMe.as_view(), name='g_p'),
    path('request_reset/', RequestPasswordReset.as_view(), name='r_resetpwd'),
    path('reset/<token>/', ResetPassword.as_view(), name='r_resetpwd'),    
    path('course/enroll/', EnrollView.as_view(), name='subcourse'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
