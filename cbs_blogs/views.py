from django.shortcuts import render
from rest_framework import viewsets
from .models import Blog, Event
from .serializers import BlogSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer   
    permission_classes = [] 

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = BlogSerializer   
    permission_classes = [] 