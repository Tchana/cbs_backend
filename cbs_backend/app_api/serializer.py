from rest_framework import serializers
from app.models import Book, Lesson

class BookSerializer(serializers.ModelSerializer):
    class Meta :
        model = Book
        fields = ['__all__']
        
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['__all__']
    