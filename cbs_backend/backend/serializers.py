
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Lesson, Course

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        User = get_user_model()
        model = User
        fields = ('email', 'password', 'role')
        
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        role = validated_data['role']
        User = get_user_model()
        user = User.objects.create_user(email=email, password=password, role=role)
        Token.objects.create(user=user)
        return user

class GetCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CreateCourseSerializer(serializers.ModelSerializer):
    User = get_user_model()
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='TEACHER'))
    class Meta:
        model = Course
        fields =  ('tilte', 'description', 'teacher')
        
    def create(self, validated_data):
        course = Course(title = validated_data['title'],
                        description=validated_data['description'],
                        teacher = validated_data['teacher']
                        )
        course.save()
        return course
    
class GetLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
    
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
            
    def create(self, validated_data):
        lesson = Lesson(title = validated_data['title'],
                        description=validated_data['description'])
        lesson.save()
        return lesson
        
