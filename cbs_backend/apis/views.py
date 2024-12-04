from rest_framework.decorators import api_view
from rest_framework.response import Response

"""
# L'api doit pouvoir recuperer des donnees depuis la base de donnees
# L'api a pour but de pouvoir inserer des donnees dans et des lecons dans la bd
# L'api a pour but de pouvoir creer des nouveaux utilisateurs
# L'api doit pouvoir gerer l'authetification(register/login/logout/)
"""

# recuperations des donnees depuis la base de donnees

@api_view(['GET'])
def getLesson(request):
    books = {'books1' : 'jose'}
    return Response(books)
    

@api_view(['POST'])
def addLesson(request):
    pass

@api_view(['GET'])
def getBooks(request):
    pass

@api_view(['POST'])
def Addcourse(request):
    pass


