
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    p_image = serializers.FileField()
    class Meta:
        User = get_user_model()
        model = User
        fields = ('firstname', 'lastname','email', 'password', 'role', 'p_image')
        
    def create(self, validated_data):
        User = get_user_model()
        
        user = User.objects.create_user(email = validated_data['email'], 
                                        password = validated_data['password'], 
                                        role = validated_data['role'],
                                        firstname = validated_data["firstname"],
                                        lastname =  validated_data["lastname"],
                                        p_image = validated_data['p_image']
                                        )
        Token.objects.create(user=user)

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only = True)
    password = serializers.CharField(write_only = True)
    
class GetTeacherSerializer(serializers.Serializer):
     class Meta :
         model = get_user_model()
         fields = ('id', 'email', 'firstname', 'lastname', 'uuid')

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                                          write_only=True,
                                          error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    confirm_password = serializers.CharField(write_only=True, required=True)
    
class GetUserSerializer(serializers.Serializer):
     class Meta :
         model = get_user_model()
         fields = ('id', 'email', 'firstname', 'lastname', 'uuid')

class GetStudentSerializer(serializers.Serializer):
     class Meta :
         model = get_user_model()
         fields = ('id', 'email', 'firstname', 'lastname')

class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'book', 'category', 'bookCover', 'description', 'language')
        
class GetBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
     
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CreateCourseSerializer(serializers.ModelSerializer):
    User = get_user_model()
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))
    class Meta:
        model = Course
        fields =  ('title', 'description', 'teacher', 'level')
        
    def create(self, validated_data):
        course = Course(title = validated_data['title'],
                        description=validated_data['description'],
                        teacher = validated_data['teacher'],
                        level = validated_data['level'])
        course.save()
        return course

class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields =  '__all__'
    
class EnrollSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.filter(role = 'student'))
    class Meta:
        model = Enrollement
        fields = ('course', 'student')
    
        def create(self, validated_data):
            enrolloment = Enrollement(student=validated_data['student'],
                                      course=validated_data['course'],
                                      )
            enrolloment.save()
            
class GetLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
    
class CreateLessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Lesson
        fields = ('course', 'title', 'file', 'description')
            
    def create(self, validated_data):
        lesson = Lesson(title = validated_data['title'],
                        description=validated_data['description'],
                        file=validated_data['file'],
                        course = validated_data['course']
                        )
        lesson.save()
        return lesson

class AudioSerializer(serializers.ModelSerializer):
    class Meta :
        model = Audio
        fields = ('title', 'description')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'description')
        
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
