from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, EventViewSet      

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'event',EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]
