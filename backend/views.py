from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import (generics,
                            permissions,
                            viewsets,
                            status)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .serializers import *
from .models import*
import os


# Create your views here.

def home(request):
    return HttpResponse('Welcome to cbs API')

class IsAdmin(permissions.BasePermission):
    '''custom permission for Admin'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class isReaders(permissions.BasePermission):
    pass

class IsNotStudent(permissions.BasePermission):
    '''custom permission for all users who are not student(admin and teacher)'''
    pass

class UserRegistrationView(generics.CreateAPIView):
    '''User registration API view'''
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class BaseManageView(APIView):
    """
    The base class for ManageViews
        A ManageView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

        return Response(status=405)

class UserLoginView(generics.CreateAPIView):
    '''User login API view'''
    serializer_class = LoginSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class EditUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, uuid):
        try:
            user = get_user_model().objects.get(uuid=uuid)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = get_user_model().objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = f"http://127.0.0.1:8000/reset/{token}"
          
            
            subject = 'Password Reset'
            message = f"""
                Dear {user.firstName}
                
                We received a request to reset your password for your account. 
                If you did not make this request, please ignore this email.
                to reset your password, please click the link below:

                {reset_url}
                
                Thank you
            """
            try :
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            except:
                pass

            return Response({'success': 'We have sent you a link to reset your password',
                             'reset_url' : f'{reset_url}'}, 
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)

class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []
    def post(self, request, token):
        User = get_user_model()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data['new_password'])
            user.save()

            reset_obj.delete()

            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=404)
        
class GetAllUserView(APIView):
    serializer_class = GetUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = get_user_model().objects.all()
        user_list = []
        if users is not None:
            for user in users:
                data = {
                    'id': user.uuid,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'role' : user.role,
                    'pImage' : request.build_absolute_uri(user.pImage.url)
                }
                user_list.append(data)
            return Response(user_list)
        
class GetUser(APIView):
    serializer_class = GetUserSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, uuid):
        try:
            user = get_user_model().objects.get(uuid=self.request.user.uuid)
            data = user
            return Response({
                'uuid': user.uuid,
                'firstame': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'pImage' : request.build_absolute_uri(user.pImage.url)
            })
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GetTeacherView(APIView):
    serializer_class = GetTeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        teachers = get_user_model().objects.filter(role='teacher')
        teacher_list = []
        for teacher in teachers:
            info = {}
            courses = Course.objects.filter(teacher=teacher.uuid)
            course_list = []
            if courses:
                for course in courses:
                    datas = {
                        'uuid' : course.uuid,
                        'title' : course.title,
                        'description' : course.description
                    }
                course_list.append(datas)
            
            info = {
                'uuid' : teacher.uuid,
                'firstName' : teacher.firstName,
                'lastName' : teacher.lastName,
                'email' : teacher.email,
                'pImage' : request.build_absolute_uri(teacher.pImage.url),
                'course' : course_list
            }
            teacher_list.append(info)
        return Response(teacher_list)
        
class GetStudentView(APIView):
    serializer_class = GetStudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        students = get_user_model().objects.filter(role="student")
        student_list = []
        if students is not None:
            for student in students:
                enrollement_list = []
                enrolled_courses = Enrollement.objects.filter(student=student.uuid)
                
                if enrolled_courses:
                    for enroll_course in enrolled_courses:
                        info ={
                            'uuid' : enroll_course.course.uuid,
                            'title' : enroll_course.course.title,
                            'description': enroll_course.course.description
                        }
                        enrollement_list.append(info)
                data = {
                    'uuid': student.uuid,
                    'firstName': student.firstName,
                    'lastName': student.lastName,
                    'email': student.email,
                    'pImage' : request.build_absolute_uri(student.pImage.url),
                    'role' : student.role,
                    'enrolled_course' : enrollement_list
                }
                student_list.append(data)
            return Response(student_list)
        
class DeleteUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, uuid):
        try:
            user = get_user_model().objects.filter(uuid = uuid).get()
            infos = user
            user.delete()
            return Response({
                'uuid': infos.uuid,
                'full_name' : infos.firstName + ' ' + infos.lastName,
                'email':  infos.email,
                'status' : 'deleted'
            })
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class GetMe(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            user = get_user_model().objects.get(uuid=self.request.user.uuid)
            return Response({
                'uuid': user.uuid,
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'pImage': request.build_absolute_uri(user.pImage.url)})
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetListCourses(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        scheme = request.scheme
        host = request.get_host()
        full_host_url = f"{scheme}://{host}"
        try:
            # Prefetch related lessons and teachers for efficiency
            courses = Course.objects.prefetch_related('lessons', 'teacher').all()
            datas = []

            for course in courses:
                data = {
                    'id': course.uuid,
                    'title': course.title,
                    'description': course.description,
                    'level': course.level,
                    'courseCover' : str(course.courseCover.url) ,
                    'teacher': {
                        'id': course.teacher.uuid,
                        'firstName': course.teacher.firstName,
                        'lastName': course.teacher.lastName,
                    },
                    'lessons': []
                }

                # Loop through the pre-fetched lessons
                for lesson in course.lessons.all():
                    lesson_data = {
                        'id': lesson.uuid,
                        'title': lesson.title,
                        'description': lesson.description,
                        'file': request.build_absolute_uri(lesson.file.url) if lesson.file else None
                    }
                    data['lessons'].append(lesson_data)
                
                datas.append(data)
            return Response(datas)
        except Exception as e:
            return Response({'error': request.build_absolute_uri(e)}, status=500)


class CreateCourseView(generics.CreateAPIView):
    '''Create course API view'''
    serializer_class = CreateCourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateCourseView(APIView):
    '''Modify course API view'''
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, uuid):
        try:
            course = Course.objects.get(uuid=uuid)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateCourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCourseView(generics.DestroyAPIView):
    '''Delete course API view'''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    
    def delete(self, request, uuid):
        course = Course.objects.filter(uuid=uuid).get()
        info = {
            'title' : course.title,
            'description' : course.description,
            'level' : course.level,
            'status' : 'deleted'
        }
        course.delete()
        return Response(info)

class CourseManagerView(BaseManageView):
    VIEWS_BY_METHOD = {
        'POST' :CreateCourseView.as_view,
        'GET': GetListCourses.as_view,
        'PATCH': UpdateCourseView.as_view,
        'DELETE': DeleteCourseView.as_view
    }


class AddLessonView(generics.CreateAPIView):
    '''Add Lesson API view'''
    queryset = Lesson.objects.all()
    serializer_class = CreateLessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class GetLesson(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetLessonSerializer
    queryset = Lesson.objects.all()
    
    def get(self, request, uuid):
        course = Course.objects.prefetch_related('lessons').get(uuid=uuid)
        data = []
        for lesson in course.lessons.all():
            lesson_data = {
                    'id': lesson.uuid,
                    'title': lesson.title,
                    'description': lesson.description,
                    'file': lesson.file.url if lesson.file else None
                    }
            data.append(lesson_data)
        
        return Response({'course_uuid' : f"{course.uuid}",
                         "lessons" : data})

class LessonManagerView(BaseManageView):
    VIEWS_BY_METHOD = {
        'POST' :AddLessonView.as_view,
        'GET': GetLesson.as_view,
    }
    
class EnrollView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EnrollSerializer


class GetLessonView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        student = get_user_model().objects.get(user=self.request.user)
        enrolled_courses = Enrollement.objects.filter(student=student, is_active=True).values_list('uuid', flat=True)
        default_course = Course.objects.filter(level='level 1').values_list('uuid')

        return (default_course, enrolled_courses)


class AddBookView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AddBookSerializer

class GetBookCategory(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetBookSerializer
    queryset = Book
    def get(self, request, category):
       books =[]
       try:
           booksInCategory = Book.objects.filter(category=category)
           for book in booksInCategory:
               info = {
               'uuid' : book.uuid,
               'title' : book.title,
               'book' : request.build_absolute_uri(book.book.url),
               'category' : book.category,
               'description' : book.description,
           }
               books.append(info)
           return Response(books, status = status.HTTP_200_OK)
       except Book.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)

class GetBookInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetBookSerializer
    queryset = Book
    def get(self, request, category):
       books =[]
       try:
           booksInCategory = Book.objects.all(category=category)
           for book in booksInCategory:
               info = {
               'uuid' : book.uuid,
               'title' : book.title,
               'book' : request.build_absolute_uri(book.book),
               'category' : book.category,
               'description' : book.description,
           }
               books.append(info)
           return Response(booksInCategory, status = status.HTTP_200_OK)
       except Book.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)

class GetBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetBookSerializer
    
    def get(self, request):
        all_books =[]
        try:
            books = Book.objects.all()
            for bk in books:
                info = {
                'uuid' : bk.uuid,
                'title' : bk.title,
                'book' : request.build_absolute_uri(bk.book.url),
                'category' : bk.category,
                'description' : bk.description,
                'author' : bk.author,
                'bookCover' : request.build_absolute_uri(bk.bookCover.url),
                'language' : bk.language
            }
                all_books.append(info)
            return Response(all_books, status = status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
class AddAudioView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AudioSerializer

class AddVideoView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VideoSerializer
