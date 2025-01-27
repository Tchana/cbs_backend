from django.shortcuts import render ,redirect, HttpResponse
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CreateCourseSerializer, GetCourseSerializer, LessonSerializer
from .models import Course, Lesson
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User = get_user_model()
            User.objects.create_user(email=email, password=password)
            return HttpResponse('Successuffuly registerd')

    form = RegisterForm()
    context = {'form':form}
        
    return render(request, 'register.html', context)


class IsAdmin(permissions.BasePermission):
    '''custom permission for Admin'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
    
class IsNotStudent(permissions.BasePermission):
    '''custom permission for all users who are not student(admin and teacher)'''
    pass


class UserRegistrationView(generics.CreateAPIView):
    '''User registration API view'''
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
class UserLoginView(APIView):
    '''User login API view'''
    permission_classes = ()
    authentication_classes = ()
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            return Response('isAuthenticated')
        else:
            return Response('isNotAuthenticated')
     
class ListCourses(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = GetCourseSerializer
    queryset = Course.objects.all()
   
class CreateCourseView(generics.CreateAPIView):
    '''Create course API view'''
    serializer_class = CreateCourseSerializer
    permission_classes = [permissions.AllowAny] 
    
    
class ModifyCourseView(generics.UpdateAPIView):
    '''Modify course API view'''
    pass

class DeleteCourseView(generics.DestroyAPIView):
    '''Delete course API view'''
    pass


class AddLessonView(generics.CreateAPIView):
    '''Add Lesson API view'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsNotStudent]
    
    
    
            



           
           