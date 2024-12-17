from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Book, Teacher, Course, Lesson, Student
from .form import RegisterForm, LessonForm, BookForm


def add_user_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get('fname')
            lname = form.cleaned_data.get('lname')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password  = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            
            #save infos to the database according to roles
            if role == '1':
                teacher = Teacher(
                    fname = fname,
                    lname = lname,
                    email = email,
                    role = role,
                )
                
                teacher.save()
                
                #create user teacher
                user = User.objects.create_user(
                username= username,
                password = password,)
                
                #login the user and him to the the corresponding page
                login(request, user)
                
                return redirect('teacher-list')
            
            if role == '2':
                
                student = Student(
                    fname = fname,
                    lname = lname,
                    email = email,
                    role = role,)
                
                student.save()
                user = User.objects.create_user(
                    username=username,
                    password=password,)
                
                login(request, user)
                return redirect('student-list')
    else:
        form = RegisterForm()
        template_name = 'admin/home.html'
        context = {'form' : form}
        return render(request, template_name, context)

def showStudentView(request):
    students = Student.objects.all()
    template_name = 'admin/student.html'
    context = {'students' : students}
    return render(request, template_name, context)


def showTeacherView(request):
    teachers = Teacher.objects.all()
    template_name = 'admin/teacher.html'
    context = {'students' : teachers}
    return render(request, template_name, context)


def deleteTeacherView(request, id):
    teacher = Teacher.objects.get(id = id)
    if request.method == 'GET':
        logout(request)
        teacher.delete()
    return redirect('teacher-list')

def deleteStudentView(request, id):
    student = Student.objects.get(id=id)
    if request.methode == 'GET' :
        logout(request)
        student.delete()
    return redirect('student-list')
        


    
    
           