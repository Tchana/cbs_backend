from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import BookSerializer, LessonSerializer
from app.models import Book
from app.models import Lesson

"""
# L'api doit pouvoir recuperer des donnees depuis la base de donnees
# L'api a pour but de pouvoir inserer des donnees dans et des lecons dans la bd
# L'api a pour but de pouvoir creer des nouveaux utilisateurs
# L'api doit pouvoir gerer l'authetification(register/login/logout/)
"""

# recuperations des donnees depuis la base de donnees
    
@api_view(['GET'])
def getBooks(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getLesson(request):
    lesson = Lesson.objects.all()
    serializer = BookSerializer(lesson, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addLesson(request):
    pass

@api_view(['POST'])
def Addcourse(request):
    pass


