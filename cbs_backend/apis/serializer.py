from rest_framework import serializers
from app.models import Books, Course, Lesson

class BookSerializer(serializers.ModelSerializer):
    class Meta :
        model = Books
        fields = ['__all__']
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['__all__']
    